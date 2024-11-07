import asyncio
from collections import defaultdict
import logging
import uuid
from ai.memo.structure.utils import preprocess_memos
from ai.memo.structure.utils.chains import connect_new_tags_chain, Connect_new_tags_output
from ai.memo.utils import get_tag_dict, get_current_structure
from ai.utils import embedder
from routers._models.memo import Memo_memo_and_tags, Memo_processed_memo, Res_post_memo_structures
from routers._models.memo._models.tag import Memo_tag


async def get_new_structures(user_id: str, memos_and_tags: list[Memo_memo_and_tags], lang: str="Korean") -> Res_post_memo_structures:
    existing_tag_dicts, current_structure_using_name, preprocessed_memos=await asyncio.gather(
        get_tag_dict(user_id),
        get_current_structure(user_id),
        preprocess_memos(memos_and_tags, lang)
    )
    _, existing_tag_name_to_id=existing_tag_dicts
    
    _connect_existing_tags(preprocessed_memos, existing_tag_name_to_id)
    embeddings, connect_new_tag_result=await asyncio.gather(
        _process_embeddings(preprocessed_memos),
        _connect_new_tags(preprocessed_memos, current_structure_using_name, lang)
    )
    
    _merge_processed_memos_and_embedding(preprocessed_memos, embeddings)
    current_structure_using_id=_get_current_structure_using_id(current_structure_using_name, existing_tag_name_to_id)
    new_structure, new_tags=_process_connect_new_tag_result(preprocessed_memos, existing_tag_name_to_id, current_structure_using_id, connect_new_tag_result)
    uniqued_new_structure=_remove_duplicated_tags(new_structure)
    
    return Res_post_memo_structures(
        processed_memos=preprocessed_memos,
        new_tags=new_tags,
        new_structure=uniqued_new_structure,
        new_reversed_structure=_get_reversed_structure(uniqued_new_structure),
    )

def _connect_existing_tags(preprocessed_memos: list[Memo_processed_memo], tag_name_to_id: dict[str, str]) -> None:
    for memo in preprocessed_memos:
        new_temporal_tag_list=[]
        updated_parent_tag_ids=[]
        
        for tag in memo.temporal_tags: # type: ignore
            if tag.name in tag_name_to_id:
                updated_parent_tag_ids.append(tag_name_to_id[tag.name])
            else:
                new_temporal_tag_list.append(tag)
                
        memo.temporal_tags=new_temporal_tag_list
        memo.parent_tag_ids=updated_parent_tag_ids

async def _connect_new_tags(preprocessed_memos: list[Memo_processed_memo], current_structure: dict[str, list[str]], lang) -> Connect_new_tags_output:
    return await connect_new_tags_chain(preprocessed_memos, current_structure, lang)
        
async def _process_embeddings(preprocessed_memos: list[Memo_processed_memo]) -> list[tuple[list[float], list[float]]]:
    logging.info("_process_embeddings] " + str(preprocess_memos))
    tasks=[ 
        asyncio.gather(
            embedder.aembed_query(memo.content),
            embedder.aembed_query(memo.metadata)
        ) for memo in preprocessed_memos
    ]
    
    return await asyncio.gather(*tasks)

def _merge_processed_memos_and_embedding(preprocessed_memos: list[Memo_processed_memo], embeddings: list[tuple[list[float], list[float]]]) -> None:
    for memo, (embedding_content, embedding_metadata) in zip(preprocessed_memos, embeddings):
        memo.embedding=embedding_content
        memo.embedding_metadata=embedding_metadata

def _process_connect_new_tag_result(preprocessed_memos: list[Memo_processed_memo], existing_tag_name_to_id: dict[str, str], current_structure_using_id: dict[str, list[str]], connect_new_tag_result: Connect_new_tags_output) -> tuple[dict[str, list[str]], list[Memo_tag]]:
    modified_structure=current_structure_using_id
    tag_name_to_id=existing_tag_name_to_id.copy()
    new_tags: list[Memo_tag]=[]
    
    for relation in connect_new_tag_result.relations:
        if relation.child_name not in tag_name_to_id:
            tag_name_to_id[relation.child_name]=str(uuid.uuid4().hex)
            new_tags.append(Memo_tag(id=tag_name_to_id[relation.child_name], name=relation.child_name, is_new=True))
        if relation.parent_name not in tag_name_to_id:
            tag_name_to_id[relation.parent_name]=str(uuid.uuid4().hex)
            new_tags.append(Memo_tag(id=tag_name_to_id[relation.parent_name], name=relation.parent_name, is_new=True))
        
    for relation in connect_new_tag_result.relations:
        child_id, parent_id=tag_name_to_id[relation.child_name], tag_name_to_id[relation.parent_name]
        if parent_id not in modified_structure:
            modified_structure[parent_id]=[]
        modified_structure[parent_id].append(child_id)
    
    for memo in preprocessed_memos:
        if memo.temporal_tags:
            for tag in memo.temporal_tags:
                memo.parent_tag_ids.append(tag_name_to_id[tag.name])
            memo.temporal_tags=None
        
    return modified_structure, new_tags

def _remove_duplicated_tags(structure: dict[str, list[str]]) -> dict[str, list[str]]:
    uniqued_structure = {}
    for parent, childs in structure.items():
        uniqued_structure[parent] = list(set(childs))
    
    return uniqued_structure

def _get_current_structure_using_id(current_structure_using_name: dict[str, list[str]], existing_tag_name_to_id: dict[str, str]) -> dict[str, list[str]]:
    structure: defaultdict[str, list[str]]=defaultdict(list[str])
    for parent, childs in current_structure_using_name.items():
        for child in childs:
            structure[existing_tag_name_to_id[parent]].append(existing_tag_name_to_id[child])
    
    return structure

def _get_reversed_structure(structure: dict[str, list[str]]) -> dict[str, list[str]]:
    reversed_structure: defaultdict[str, list[str]]=defaultdict(list[str])
    for parent, childs in structure.items():
        for child in childs:
            reversed_structure[child].append(parent)
    
    return reversed_structure
        

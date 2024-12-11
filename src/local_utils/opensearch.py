import copy
from typing import List, Tuple
from opensearchpy import OpenSearch, RequestsHttpConnection
import boto3
from requests_aws4auth import AWS4Auth
import time

class opensearch_utils():
    
    @classmethod
    def create_aws_opensearch_client(cls, region: str, host: str) -> OpenSearch:
        """
        서버리스 OpenSearch 클라이언트 생성
        """
        service = 'aoss'
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            region,
            service,
            session_token=credentials.token
        )

        # OpenSearch 클라이언트 생성
        client = OpenSearch(
            hosts=[{
                'host': host.replace("https://", ""),
                'port': 443
            }],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            timeout=300
        )

        # 데이터 액세스 규칙이 적용될 때까지 대기
        time.sleep(45)
        
        return client

    @classmethod
    def create_index(cls, os_client, index_name, index_body):
        '''
        인덱스 생성
        '''
        try:
            response = os_client.indices.create(
                index_name,
                body=index_body
            )
            print('\nCreating index:')
            print(response)
            return response
        except Exception as e:
            print(f"Error creating index: {str(e)}")
            raise e

    @classmethod
    def check_if_index_exists(cls, os_client, index_name):
        '''
        인덱스가 존재하는지 확인
        '''
        try:
            exists = os_client.indices.exists(index_name)
            print(f"index_name={index_name}, exists={exists}")
            return exists
        except Exception as e:
            print(f"Error checking index existence: {str(e)}")
            raise e

    @classmethod
    def add_doc(cls, os_client, index_name, document, id):
        '''
        # Add a document to the index.
        '''
        response = os_client.index(
            index = index_name,
            body = document,
            id = id,
            refresh = True
        )

        print('\nAdding document:')
        print(response)

    @classmethod
    def search_document(cls, os_client, query, index_name):
        response = os_client.search(
            body=query,
            index=index_name
        )
        #print('\nKeyword Search results:')
        return response

    @classmethod
    def delete_index(cls, os_client, index_name):
        response = os_client.indices.delete(
            index=index_name
        )

        print('\nDeleting index:')
        print(response)

    @classmethod
    def parse_keyword_response(cls, response, show_size=3):
        '''
        키워드 검색 결과를 보여 줌.
        '''
        length = len(response['hits']['hits'])
        if length >= 1:
            print("# of searched docs: ", length)
            print(f"# of display: {show_size}")        
            print("---------------------")        
            for idx, doc in enumerate(response['hits']['hits']):
                print("_id in index: " , doc['_id'])
                print(doc['_score'])
                print(doc['_source']['text'])
                print(doc['_source']['metadata'])
                print("---------------------")
                if idx == show_size-1:
                    break
        else:
            print("There is no response")

    @classmethod
    def opensearch_pretty_print_documents(cls, response):
        '''
        OpenSearch 결과인 LIST 를 파싱하는 함수
        '''
        for doc, score in response:
            print(f'\nScore: {score}')
            print(f'Document Number: {doc.metadata["row"]}')

            # Split the page content into lines
            lines = doc.page_content.split("\n")

            # Extract and print each piece of information if it exists
            for line in lines:
                split_line = line.split(": ")
                if len(split_line) > 1:
                    print(f'{split_line[0]}: {split_line[1]}')

            print("Metadata:")
            print(f'Type: {doc.metadata["type"]}')
            print(f'Source: {doc.metadata["source"]}')        

            print('-' * 50)

    
    # def get_document(cls, os_client, doc_id, index_name):
    #     response = os_client.get(
    #         id= doc_id,
    #         index=index_name
    #     )

    #     return response
    @classmethod
    def get_document(cls, os_client, doc_id, index_name):
        print(doc_id, index_name)
        try:
            # 문서 조회 시도
            response = os_client.search(
                index=index_name,
                body={
                    "query": {
                        "match": {
                            "_id": doc_id
                        }
                    }
                }
            )
            
            # 결과가 있는지 확인
            if response['hits']['total']['value'] > 0:
                return response['hits']['hits'][0]
            else:
                print(f"Document with ID {doc_id} not found")
                return None
                
        except Exception as e:
            print(f"Error retrieving document: {str(e)}")
            return None

    @classmethod
    def get_count(cls, os_client, index_name):
        response = os_client.count(
            index=index_name
        )

        return response

    @classmethod
    def get_query(cls, **kwargs):

        # Reference:
        # OpenSearcj boolean query:
        #  - https://opensearch.org/docs/latest/query-dsl/compound/bool/
        # OpenSearch match qeury:
        #  - https://opensearch.org/docs/latest/query-dsl/full-text/index/#match-boolean-prefix
        # OpenSearch Query Description (한글)
        #  - https://esbook.kimjmin.net/05-search)

        search_type = kwargs.get("search_type", "lexical")

        if search_type == "lexical":

            min_shoud_match = 0
            if "minimum_should_match" in kwargs:
                min_shoud_match = kwargs["minimum_should_match"]

            QUERY_TEMPLATE = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "text": {
                                        "query": f'{kwargs["query"]}',
                                        "minimum_should_match": f'{min_shoud_match}%',
                                        "operator":  "or",
                                        # "fuzziness": "AUTO",
                                        # "fuzzy_transpositions": True,
                                        # "zero_terms_query": "none",
                                        # "lenient": False,
                                        # "prefix_length": 0,
                                        # "max_expansions": 50,
                                        # "boost": 1
                                    }
                                }
                            },
                        ],
                        "filter": [
                        ]
                    }
                }
            }

            if "filter" in kwargs:
                QUERY_TEMPLATE["query"]["bool"]["filter"].extend(kwargs["filter"])

        elif search_type == "semantic":

            QUERY_TEMPLATE = {
            "query": {
                    "bool": {
                        "must": [
                            {
                                "knn": {
                                    kwargs["vector_field"]: {
                                        "vector": kwargs["vector"],
                                        "k": kwargs["k"],
                                    }
                                }
                            },
                        ],
                        "filter": [
                        ]
                    }
                }
            }

            if "filter" in kwargs:
                QUERY_TEMPLATE["query"]["bool"]["filter"].extend(kwargs["filter"])

        return QUERY_TEMPLATE

    @classmethod
    def get_filter(cls, **kwargs):

        BOOL_FILTER_TEMPLATE = {
            "bool": {
                "filter": [
                ]
            }
        }

        if "filter" in kwargs:
            BOOL_FILTER_TEMPLATE["bool"]["filter"].extend(kwargs["filter"])

        return BOOL_FILTER_TEMPLATE

    @staticmethod
    def get_documents_by_ids(os_client, ids, index_name):

        response = os_client.mget(
            body={"ids": ids},
            index=index_name
        )

        return response

    @staticmethod
    def opensearch_pretty_print_documents_with_score(response):
        '''
        OpenSearch 결과인 LIST 를 파싱하는 함수
        '''
        responses = copy.deepcopy(response)
        for doc, score in responses:
            print(f'\nScore: {score}')
            # print(f'Document Number: {doc.metadata["row"]}')
            # Split the page content into lines
            lines = doc.page_content.split("\n")
            metadata = doc.metadata
            if "image_base64" in metadata: metadata["image_base64"] = ""
            if "orig_elements" in metadata: metadata["orig_elements"] = ""
            
            print(lines)
            print(metadata)

    @staticmethod
    def get_all_documents(os_client, index_name, size=10):
        try:
            response = os_client.search(
                index=index_name,
                body={
                    "query": {
                        "match_all": {}
                    }
                },
                size=size
            )
            return response['hits']['hits']
        except Exception as e:
            print(f"Error retrieving documents: {str(e)}")
            return None

    @classmethod
    def get_document_safe(cls, os_client, doc_id, index_name):
        try:
            # 문서 조회 시도
            response = os_client.search(
                index=index_name,
                body={
                    "query": {
                        "match": {
                            "_id": doc_id
                        }
                    }
                }
            )
            
            # 결과가 있는지 확인
            if response['hits']['total']['value'] > 0:
                return response['hits']['hits'][0]
            else:
                print(f"Document with ID {doc_id} not found")
                return None
                
        except Exception as e:
            print(f"Error retrieving document: {str(e)}")
            return None

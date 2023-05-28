import re
import json


class RequestParser():
    
    def __init__(self) -> None:
        pass
        
    @staticmethod
    def extract_body(request: str) -> dict or None:
        body = re.findall("\n(\{[^}]+\})", request)
        if body:
            body = body[0]
            body.replace('\n', '')
            return json.loads(body)
        return {}
    
    @staticmethod
    def extract_headers(request: str) -> list[str]:
        extract = re.findall("(^[^\{]+)\n\{", request)
        if extract:
            return extract[0].strip().replace('\r', '').split('\n')
        return request.replace('\r', '').split('\n')
    
    @staticmethod
    def extract_cookie(request: str) -> dict:
        extract = re.findall("Cookie\:\s([^\n]+)", request)
        cookie_dict = {}
        
        if extract:
            extract = extract[0].replace('\r', '').split(',')
            for item in extract:
                splitted_item = item.split('=')
                cookie_dict[splitted_item[0]] = splitted_item[1]
        return cookie_dict
    
    def parse_request(self, request: str) -> dict:
        req_dict = {}
        # extract headers from request
        headers_arr = self.extract_headers(request=request)
        if len(headers_arr) > 0:
            # Parse method header
            method_path_arr = headers_arr[0].split(' ')
            req_dict['method'] = method_path_arr[0]
            req_dict['path'] = method_path_arr[1]
            req_dict['protocol'] = method_path_arr[2]
            
            # Handle the rest of the headers
            for header in headers_arr[1:]:
                if len(header) > 1:
                    header_split = header.split(':')
                    req_dict[header_split[0]] = header_split[1].strip()
        # Set request body in dictionary
        req_dict['body'] = self.extract_body(request=request)
        return req_dict

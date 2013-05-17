'''
Created on May 5, 2013

@author: dorisip
'''
import os
from pycparser import parse_file
import copy
from pycparser.c_ast import ArrayDecl, IdentifierType, Struct, \
    TypeDecl
from windy_tales.database.collections.header_file_parsed_template import HeaderfileParsedTemplate
from windy_tales.exceptions.exceptions import HeaderFileNotFound
from cloudy_tales.database.connectionManager import DbConnectionManager


class HeaderParser():
    '''
    Parser for C header file
    Parses to json format
    '''

    @staticmethod
    def generate_tempate(file_name=None):
        # Assumption: we only have one header file
        if file_name is None:
            os.environ['PATH'] += os.pathsep + '/usr/bin'
            here = os.path.abspath(os.path.dirname(__file__))
            file_name = os.path.join(here, '..', 'resources', 'test.h')

        return HeaderParser.__parse_c_header_file(file_name)

    @staticmethod
    def get_template(name):
        '''
        Return read from mongoDB
        '''
        with DbConnectionManager() as connection:
            headerFileParsedTemplate = HeaderfileParsedTemplate(connection=connection)
            json = headerFileParsedTemplate.find_by_name(name)
            if json is None:
                raise HeaderFileNotFound(name)
            result = json.get('metadata')
        return result

    @staticmethod
    def __parse_c_header_file(file_name):
        '''
        Parses a C header file, returning an AST representation
        '''
        os.environ['PATH'] += os.pathsep + '/usr/bin'

        # Calls pycparser to precompile and parse the C header file
        ast = parse_file(file_name, use_cpp=True, cpp_path='/usr/bin/cpp')
        # Prints out parsed file structure for debugging
        # HeaderParser.ast.show(attrnames=True, nodenames=True)

        # Theoretically there should only be one struct per header file
        if len(ast.ext) > 1:
            print("Warning, header file has more than 1 struct.  Only the first one will be used")

        return HeaderParser.__parse_ast_to_json(ast.ext[0])

    @staticmethod
    def __parse_ast_to_json(node):
        '''
        Given an AST node, creates an ordered dict representing the structure of the header file
        from header:
        struct address {
            char address_line1[20];
            char country[2];
        };
        generates the following ordered dict: {"address": [{"address_line1": 20}, {"country": 2}]}
        '''
        result = {}
        node_type = node.type

        if node_type.name:
            struct_name = node_type.name
        elif node_type.declname:
            struct_name = node_type.declname

        result[struct_name] = []
        for decl in node_type.decls:
            decl_type = decl.type
            if type(decl_type) is ArrayDecl:
                __size = int(decl_type.dim.value)
                __type = decl_type.type.type
                __name = decl_type.type.declname
                if type(__type) is IdentifierType:
                    __format = __type.names[0]
                    result[struct_name].append({__name: __size})
                elif type(__type) is Struct:
                    struct_result = HeaderParser.__parse_ast_to_json(decl_type.type)
                    # Note that there should only have one key
                    __name = struct_result.keys()[0]
                    __list = []
                    for i in range(__size):
                        # Make a deep copy of the json object
                        __list.append(copy.deepcopy(struct_result[__name]))
                    result[struct_name].append({__name: __list})
            elif type(decl_type) is TypeDecl:
                if type(decl_type.type) is Struct:
                    struct_result = HeaderParser.__parse_ast_to_json(decl_type)
                    # Note that there should only have one key
                    __name = struct_result.keys()[0]
                    result[struct_name].append({__name: struct_result[__name]})
                elif type(decl_type.type) is IdentifierType:
                    # datatypes such as int falls into here
                    pass
        return result

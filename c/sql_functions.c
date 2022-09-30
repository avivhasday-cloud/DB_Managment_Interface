#include <stdio.h>
#include <stdlib.h>
#include <mysql.h>
#include <string.h>

typedef int Bool;
#define True 1
#define False 0


static char *socket = NULL;
unsigned int port = 3306;
unsigned int flags = 0;

struct User
{
	int id;
	char full_name[64];
	char email[128];
	char hash_password[256];
};

enum table
{
    USERS
};


void print_db_error(MYSQL *conn){
	printf("%s\n Connection Error #:[%d]\n", mysql_error(conn), mysql_errno(conn));
}

/**
 * @brief this function tries to connect to mysql by given creditianls
 * 		  returns mysql connection handler on successfull login else NULL
 * 
 * @param conn mysql object
 * @param host host name
 * @param user username
 * @param pass password
 * @param db database name
 * @param port mysql service port
 * @param unix_socket unix socket
 * @param flag client flags
 * @return MYSQL connection handler
 */
Bool connect_to_mysql(MYSQL *conn, const char *host, const char *user, const char *pass, const char *db, unsigned int port, const char *unix_socket, unsigned int flag){
	
	if (!mysql_real_connect(conn, host, user, pass, db, port, socket, flags)) {
		print_db_error(conn);
		return False;
	}
	printf("%s", "Connected successfully\n");
	return True;
}

Bool connect_to_db(MYSQL *conn, const char *db){
	return (!mysql_select_db(conn, db)) ?  True : False;
}

MYSQL_RES* execute_query(MYSQL *conn, const char *statment_str){
    MYSQL_RES* query_res = NULL;
    if (mysql_query(conn, statment_str) == 0){
        query_res = mysql_store_result(conn);
    }
    return query_res;
}

int copy_query_results_to_buffer(MYSQL_RES* query_results, char* buffer){
    
    int counter = 0;
    char* field;
    int num_of_results = 0;
    do
    {
        MYSQL_ROW row = mysql_fetch_row(query_results);
        if (row == 0)
        {
            break;
        }
        for (int i=0; i < mysql_num_fields(query_results); i++)
        {
            field = row[i] ? row[i] : "NULL";
            int length = strlen(field);
            if (counter + length + 1 > 4096)
            {
                break;          
            } 
            memcpy(buffer + counter, field, length + 1);   
            counter += length + 1;
            num_of_results++;
        }
    } while(True);
    return num_of_results;

}

void free_results_ptr(MYSQL_RES* query_results){
    mysql_free_result(query_results);
}

int get_databases(MYSQL* conn, const char* wild, char* buffer){
    MYSQL_RES* query_results = mysql_list_dbs(conn, wild);
    if (query_results){
        int num_of_results = copy_query_results_to_buffer(query_results, buffer);
        free_results_ptr(query_results);
        return num_of_results;
    }
    return 0;
}

char* get_table_name(MYSQL_RES* query_results){
    return query_results->fields->table;
}

char* get_database_name(MYSQL* conn){
    return conn->db;
}

int get_results(MYSQL_RES* query_results, char* buffer){
    int num_of_results = copy_query_results_to_buffer(query_results, buffer);
    free_results_ptr(query_results);
    return num_of_results;
}

int execute_query_and_get_results(MYSQL * conn, const char* statment_str, char *buffer) {
    MYSQL_RES* query_results = execute_query(conn, statment_str);
    if (!query_results)
    {
        return 0;
    }
    else
    {
        return get_results(query_results, buffer);
    }
}

MYSQL * init_mysql_object(){
	return mysql_init(NULL);
}

void close_connection_to_mysql(MYSQL * conn){
	mysql_close(conn);
    printf("%s", "Closed connection to mysql\n");
}







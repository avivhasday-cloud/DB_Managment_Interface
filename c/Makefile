Output: sql_functions.c 
	gcc -o libsqlfunc.so -fpic -shared sql_functions.c `mysql_config --cflags --libs`

Execute: sql_functions.c
	gcc -o output sql_functions.c `mysql_config --cflags --libs`


clean:
	rm -r *.so
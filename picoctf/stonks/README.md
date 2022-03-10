# Stonks
Category: Binary exploitation, 20 points

## Description

> I decided to try something noone else has before. I made a bot to
automatically trade stonks for me using AI and machine learning. I wouldn't
believe you if you told me it's unsecure! vuln.c nc mercury.picoctf.net 16439

## Solution

After checking the connecting to the server, and looking into `vuln.c` we
notice that the `buy_stonks` function which accepts user's input, is using a
user provided string as a format string for a call of `printf`, specifically
this section of the code:

```
    char *user_buf = malloc(300 + 1);
	printf("What is your API token?\n");
	scanf("%300s", user_buf);
	printf("Buying stonks with token:\n");
	printf(user_buf);
```

This is a [Uncontrolled format string](https://en.wikipedia.org/wiki/Uncontrolled_format_string) vulnerability.


In addition to that the flag is read in this same `buy_stonks` function from a
file:

```
    char api_buf[FLAG_BUFFER];
    printf("api_buf address: %p\n", api_buf);
	FILE *f = fopen("api","r");
	if (!f) {
		printf("Flag file not found. Contact an admin.\n");
		exit(1);
	}
	fgets(api_buf, FLAG_BUFFER, f);
```

So the idea is to provide format string that can show us the contents of
`api_buf`.


After a few experiments with the local version of the program, adding `%p`, we
know then what kind of string to supply that would allow us to check the
contents, but it would also need to be decoded into chars.


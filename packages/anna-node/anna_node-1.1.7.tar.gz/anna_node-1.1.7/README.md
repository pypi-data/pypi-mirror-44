# anna
**End-to-end website testing software using selenium**

### Usage
I've made docker containers for [firefox](https://github.com/patrikpihlstrom/docker-anna-firefox) & [chrome](https://github.com/patrikpihlstrom/docker-anna-chrome),
as well as a [RESTful API](https://github.com/patrikpihlstrom/anna-api).

Run ```anna```

| arg | description             |required|
|-----|-------------------------|---------------|
| -d  | specify the driver|yes|
| -s  | specify the site|yes|
| -h  | display help|no|
| -v  | verbose mode|no|
| -H  | run in headless mode|no|
| -r  | specify the resolution of the drivers (defaults to 1920x1080)|no|
| -i  | set the id (used by [anna-api](https://github.com/patrikpihlstrom/anna-api))|no|

### Test definitions
Test cases are defined in the ```tests/anna/``` directory. Each website should have
a json file as well as a subdirectory under ```tests/anna/``` containing test definitions.
If a test is referenced, but not defined for a particular website,
anna will use the ```base``` directory as a fallback.
Consider the following file structure:
```
anna/
    tasks/
    	anna/
		example.json
		base/
			do_thing.json
		example/
			go_to_page.json
```

Example website configuration (```tests/anna/example.json```):
```
{
  "url": "https://example.com",
  "sequence": {
    "0": "do_thing",
    "1": "go_to_page"
  }
}
```
Example test definition (```tests/anna/example/go_to_page.json```):
```
{
  "events": [
    {
      "type": "click",
      "target": ".target-class"
    },
    ...
  ],
  "assertions": [
    {
      "type": "current_url",
      "is": "https://example.com/page/"
    },
    ...
  ]
}
```

### Currently implemented event types
* click ```{"type": "click", "target": "#unique_element}```
* sendkeys ```{"type": "sendkeys", "target": "#unique_element}```
* submit ```{"type": "submit", "target": "#unique_element}```
* hover ```{"type": "hover", "target": "#unique_element}```
* wait ```{"type": "wait", "target": "#unique_element}``` Waits for a target element to become visible
* switch_to ```{"type": "switch_to", "target": "#unique_element}``` Changes the focus to an iframe

### Currently implemented assertion types
* current_url ```{"in": "somepage"}``` or ```{"is": "https://example.com/somepage"}```
* element_exists ```{"target": ".some-class"}```

#### TODO
* credentials-pool using -i from anna-api
* database assertions
* subroutine processing

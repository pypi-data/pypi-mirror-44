
**Data Sourcing**

Action | Purpose
--- | ---
[execute](#execute)|Execute a command and produce the execution result
[insert](#insert)|Insert an item
[iterate](#iterate)|Iterate the configuration item producing each element
[merge](#merge)|Merge input and configuration items
[read from clock](#read-from-clock)|Produce the system clock time at regular intervals
[read from file](#read-from-file)|Produce metadata/content from a local or remote file
[read from file list](#read-from-file-list)|Produce the list of files matching a pattern
[read from file status](#read-from-file-status)|Get path status information
[read from openpipe actions](#read-from-openpipe-actions)|Produce the list of available action actions
[read from url](#read-from-url)|Produce metadata/content from an URL

**Data Selection**

Action | Purpose
--- | ---
[select](#select)|Select input items based on a conditional expression
[select subset](#select-subset)|Select a subset of data from a dictionary input

**Data Transformation**

Action | Purpose
--- | ---
[decompress](#decompress)|Decompress gzip input item
[reduce](#reduce)|Reduce a complex item type into a simpler structure
[transform using csv](#transform-using-csv)|Produce dictionary from CSV line based input
[transform using regex assign](#transform-using-regex-assign)|Build a dictionary from a key/map regex group expression

**Data Analysis**

Action | Purpose
--- | ---
[count](#count)|Count the number of elements received
[group by stats](#group-by-stats)|Produce statistics by grouping input items by keys
[pprint](#pprint)|Pretty print an item
[print](#print)|Print an item
[transform using terminaltables](#transform-using-terminaltables)|Produce a text table

**Data Control**

Action | Purpose
--- | ---
[limit](#limit)|Limit the max number of items sent to the next action
[limit running platform](#limit-running-platform)|Produce items only when running on the specified platform
[send to segment](#send-to-segment)|Send a copy of the input item to other segment(s)
[tag](#tag)|Tag input item with the provided configuration tag item
[tag key](#tag-key)|Tag a key or list of keys

**Data Export**

Action | Purpose
--- | ---
[write to file](#write-to-file)|Write item to a file

**Data Manipulation**

Action | Purpose
--- | ---
[drop](#drop)|Remove some keys from the input item
[sort](#sort)|Sort items by keys
[update](#update)|Update values depending on conditional expressions
[update using key mapping](#update-using-key-mapping)|Map values from source keys to values on target keys
[update using string replace](#update-using-string-replace)|Replace some phrase with other phrase

**Data Validation**

Action | Purpose
--- | ---
[assert](#assert)|Asserts that input matches the config provided item


## Data Sourcing

### execute
Execute a command and produce the execution result



**Required Configuration**
```yaml
    - execute:
        cmd:    # The command to be executed
```

**Optional Configuration**
```yaml
        shell:  True    # Execute the command as parameters to a system shell
        output_as_text: True # Output the command output as text
        fail_on_error: True  # Abort pipeline if exit code is not zero
```



Module source: [openpipe/actions/execute_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/execute_.py)

----


### insert
Insert an item


**Required Configuration**
```yaml
    - insert:         # Item to be produced as an output
```





Module source: [openpipe/actions/insert_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/insert_.py)

----


### iterate
Iterate the configuration item producing each element




**Optional Configuration**
```yaml
    - iterate:
        $_$     # The item to be iterated over
```



Module source: [openpipe/actions/iterate_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/iterate_.py)

----


### merge
Merge input and configuration items




**Optional Configuration**
```yaml
    - merge:
        $_tag$ # The item to merge with
```



Module source: [openpipe/actions/merge_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/merge_.py)

----


### read from clock
Produce the system clock time at regular intervals




**Optional Configuration**
```yaml
    - read from clock:
        interval:   0   # Pause time between insertions, 0 means forever
        max_count:  1     # Max number of item insertions
```



Module source: [openpipe/actions/read/from/clock_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/read/from/clock_.py)

----


### read from file
Produce metadata/content from a local or remote file



**Required Configuration**
```yaml
    - read from file:
        path:                       # Local path or HTTP/HTTPS/FTP url
```

**Optional Configuration**
```yaml
        # The mime_type will be used by the action to identify and automatically
        # decode the file content.
        # With the default value of 'auto' the action will try to guess the
        # mime type based on the content header or file extension.
        mime_type:  auto

        # The following option is only applicable to local filenames
        auto_expand_home: True      # Expand '~' on path to user home dir
```



Module source: [openpipe/actions/read/from/file_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/read/from/file_.py)

----


### read from file list
Produce the list of files matching a pattern




**Optional Configuration**
```yaml
    - read from file list:
        $_$     # The pattern to be used for matching
```



Module source: [openpipe/actions/read/from/file/list_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/read/from/file/list_.py)

----


### read from file status
Get path status information




**Optional Configuration**
```yaml
    - read from file status:
        $_$         # Path of the file to be checked
```



Module source: [openpipe/actions/read/from/file/status_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/read/from/file/status_.py)

----


### read from openpipe actions
Produce the list of available action actions




**Optional Configuration**
```yaml
    - read from openpipe actions:
        $_$     # The item to be printed, the default is the input item
```



Module source: [openpipe/actions/read/from/openpipe/actions_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/read/from/openpipe/actions_.py)

----


### read from url
Produce metadata/content from an URL



**Required Configuration**
```yaml
    - read from url:
        url:                       # HTTP/HTTPS/FTP url
```

**Optional Configuration**
```yaml
        # The mime_type will be used by the action to identify and automatically
        # decode the file content.
        # With the default value of 'auto' the action will try to guess the
        # mime type based on the content header or file extension.
        mime_type:  auto

        # The following options are only relevant for HTTP/HTTPS/FTP paths
        timeout: 30                 # Global timeout (in secs) for the operation
        ignore_http_errors: False   # Ignore HTTP errors replies
        user_agent: curl/7.64.0     # User-agent to use on HTTP requests
```



Module source: [openpipe/actions/read/from/url_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/read/from/url_.py)

----

## Data Selection

### select
Select input items based on a conditional expression


**Required Configuration**
```yaml
    - select:  # Boolean Expression
        # Items are only copied to next action only when the expression evaluates
        # to True
```





Module source: [openpipe/actions/select_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/select_.py)

----


### select subset
Select a subset of data from a dictionary input


**Required Configuration**
```yaml
    - select subset:         # YAML describing the elements to be retrieved
```





Module source: [openpipe/actions/select/subset_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/select/subset_.py)

----

## Data Transformation

### decompress
Decompress gzip input item




**Optional Configuration**
```yaml
    - decompress:
        path:   ""      # If not provided the input item is used
        type:   gzip    # the type to decompress
```



Module source: [openpipe/actions/decompress_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/decompress_.py)

----


### reduce
Reduce a complex item type into a simpler structure




**Optional Configuration**
```yaml
    - reduce:
        $_$     # The target reduction format
```



Module source: [openpipe/actions/reduce_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/reduce_.py)

----


### transform using csv
Produce dictionary from CSV line based input




**Optional Configuration**
```yaml
    - transform using csv:
            delimiter: ","          # One-character string used to separate fields
            quotechar: '"'          # One-character to wrap string values
            auto_number: False      # Attempt to convert fields to numbers
            ignore_errors: False    # Ignore conversion errors
            field_list: []          # Optional list of fields to be used as headers
```



Module source: [openpipe/actions/transform/using/csv_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/transform/using/csv_.py)

----


### transform using regex assign
Build a dictionary from a key/map regex group expression



**Required Configuration**
```yaml
    - transform using regex assign:
        regex:      # A regex expression that must match two groups:
                    # (group1) (group2)
```




Module source: [openpipe/actions/transform/using/regex/assign_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/transform/using/regex/assign_.py)

----

## Data Analysis

### count
Count the number of elements received




**Optional Configuration**
```yaml
    - count:
        group_by:   ""  # Expression to use for count aggregation
```



Module source: [openpipe/actions/count_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/count_.py)

----


### group by stats
Produce statistics by grouping input items by keys



**Required Configuration**
```yaml
    - group by stats:
        keys:         # List of keys to be used for grouping
```

**Optional Configuration**
```yaml
        stats: [sum, count, max, min]   # List of stats to obtain
        sorted_fields: []               # When these fields change, produce the sort
```



Module source: [openpipe/actions/group/by/stats_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/group/by/stats_.py)

----


### pprint
Pretty print an item




**Optional Configuration**
```yaml
    - pprint:
        $_$     # The content to be pretty printed
```



Module source: [openpipe/actions/pprint_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/pprint_.py)

----


### print
Print an item




**Optional Configuration**
```yaml
    - print:
        $_$     # The item to be printed, the default is the input item
```



Module source: [openpipe/actions/print_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/print_.py)

----


### transform using terminaltables
Produce a text table



**Required Configuration**
```yaml
    - transform using terminaltables:
        header:     # List of labels to be used as column headers
        keys:       # List of keys to be used or row elements
```




Module source: [openpipe/actions/transform/using/terminaltables_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/transform/using/terminaltables_.py)

----

## Data Control

### limit
Limit the max number of items sent to the next action



**Required Configuration**
```yaml
    - limit:
        max:    # The max number of items sent to next action
```




Module source: [openpipe/actions/limit_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/limit_.py)

----


### limit running platform
Produce items only when running on the specified platform



**Required Configuration**
```yaml
    - limit running platform:
        system:    # The system name, e.g. 'Linux', 'Windows' 'Darwin'
```




Module source: [openpipe/actions/limit/running/platform_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/limit/running/platform_.py)

----


### send to segment
Send a copy of the input item to other segment(s)



**Required Configuration**
```yaml
    - send to segment:
        name:               # Name or list of of segments to receive the item
```

**Optional Configuration**
```yaml
        when:   ""  # An expression that should result in a boolean

        # If `when` is set, item will only be copied to the segment(s)
        # when it evaluates to True. And sent to next action when it evaluates
        # to False
```



Module source: [openpipe/actions/send/to/segment_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/send/to/segment_.py)

----


### tag
Tag input item with the provided configuration tag item




**Optional Configuration**
```yaml
    - tag:
        $_$     #  Default is to tag the entire input item
```



Module source: [openpipe/actions/tag_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/tag_.py)

----


### tag key
Tag a key or list of keys



**Required Configuration**
```yaml
    - tag key:
        name:   #  The name or list of names for the keys to be tagged
```




Module source: [openpipe/actions/tag/key_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/tag/key_.py)

----

## Data Export

### write to file
Write item to a file



**Required Configuration**
```yaml
    - write to file:
        path:                   # Filename of the file to create/overwrite/append
```

**Optional Configuration**
```yaml
        content: $_$            # Content to be written to the file
        mode: "w"               # Open file mode (write/append)
        close_on_item: False    # Force file close after each received item
```



Module source: [openpipe/actions/write/to/file_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/write/to/file_.py)

----

## Data Manipulation

### drop
Remove some keys from the input item


**Required Configuration**
```yaml
    - drop: # name or list of names of the keys to be removed
```





Module source: [openpipe/actions/drop_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/drop_.py)

----


### sort
Sort items by keys



**Required Configuration**
```yaml
    - sort:
        key:                    # Name or list of names to use a group key
```

**Optional Configuration**
```yaml
        descendent: False       # Use descendent order ?

        # It is possible to identify groups of repeated keys by setting
        # key_on_first. When it's set, the key will only be present on the
        # first item of a group items with the repeated key
        key_on_first: False
```



Module source: [openpipe/actions/sort_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/sort_.py)

----


### update
Update values depending on conditional expressions



**Required Configuration**
```yaml
    - update:
        set:            # Dictionary with keys/values to be updated
```

**Optional Configuration**
```yaml
        where:  True    # Expression to select items to be updated
        else:   {}      # Dictionary with keys/values to be updated when 'where' is False
```



Module source: [openpipe/actions/update_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/update_.py)

----


### update using key mapping
Map values from source keys to values on target keys


**Required Configuration**
```yaml
    - update using key mapping:  # Dictionary with the key mapping :
        #
        #   target_key_name:
        #       source_key_name:
        #           old_value: new_value
        #
        #  The action will set the "target_key_name" to "new_value" when the value
        #  at source_key_name is equal to "old_value"
```





Module source: [openpipe/actions/update/using/key/mapping_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/update/using/key/mapping_.py)

----


### update using string replace
Replace some phrase with other phrase


**Required Configuration**
```yaml
    - update using string replace:  # Dictionary with the replacement rules:
        # Replacement rules for a single string input item:
        #
        #   { "search_string" : "replace_string", ... }
        #   Replaces all occurrences of search_string with replace_string
        #
        #   source_key_name:
        #       "search_string" : "replace_string"
        #
        #  In the 'source_key_name' value replaces all occurrences of
        # 'search_string' with 'replace_string' in the
```





Module source: [openpipe/actions/update/using/string/replace_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/update/using/string/replace_.py)

----

## Data Validation

### assert
Asserts that input matches the config provided item


**Required Configuration**
```yaml
    - assert:         # The item with the expected value(s)
```





Module source: [openpipe/actions/assert_.py](https://github.com/Openpipe/openpipe/blob/master/openpipe/actions/assert_.py)

----

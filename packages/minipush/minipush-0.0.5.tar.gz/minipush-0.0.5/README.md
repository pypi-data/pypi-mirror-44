# minipush by Rémi "Mr e-RL" LANGDORPH
## (c)2019 Rémi LANGDORPH - mrerl@warlegend.net

### This package supports the followings filetypes: css, js

# Sample config:
```json
{
    "origin": {"folders":["css/", "js/core/", "js/plugins/", "js/"]},
    "destination": {"folder": "../templates/", "exts": ["htm", "html"], "type": "embed", "basefolderlink": "/static/"},
    "anchors": {"js": {"start": "<!--AutomatedJSExport-Start-->",
                "end": "<!--AutomatedJSExport-End-->"},
                "css": {"start": "<!--AutomatedCSSExport-Start-->",
                        "end": "<!--AutomatedCSSExport-End-->"},
                "conf": {"start": "<!--AutomatedExport-Start->",
                        "end": "<-AutomatedExport-End-->"}
                },
    "format":{"embed":{"js": "<!--{filename}--><script>{content}</script>",
                       "css": "<!--{filename}--><style>{content}</style>"},
              "link":{"js": "<script src='{path}'/>",
                      "css": "<link href='{path}' rel='stylesheet'/>"}
            },
    "cache": {"folder": "../static/",
              "enabled": true}
}
```
# Example script:
```python
from minipush import Minipush
Minipush(file="config.json").run()
```

# Command mode:
## python -m minipush *arguments*
```
Arguments:
command      argument         description
-c --config  {configfile}     set the json config file to load
-j --json    '{configjson}'   set the config from json
-r --reset                    remove all the scripts from the templates
-h --help                     show help
```

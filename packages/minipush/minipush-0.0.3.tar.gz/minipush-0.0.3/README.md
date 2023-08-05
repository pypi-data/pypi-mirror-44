minipush by Rémi "Mr e-RL" LANGDORPH
(c)2019 Rémi LANGDORPH - mrerl@warlegend.net

This lib supports the followings filetypes: css, js

Sample config:
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

Example script:
from minipush import Minipush
Minipush(file="config.json").run()

Don't hesitate to use the 'python -m minipush' (-h to see help)

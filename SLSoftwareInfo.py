# -*- coding: utf-8 -*-

software_info = {
    '7-Zip': {
        'DownloadURL': 'http://www.7-zip.org/',
        'CheckUpdateURL': 'http://www.7-zip.org/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'7-Zip'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Download 7-Zip ([\d.]+) \((?:\d{4}-\d{1,2}-\d{1,2})\) for Windows'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'Download 7-Zip (?:[\d.]+) \((\d{4}-\d{1,2}-\d{1,2})\) for Windows'
        }
    },
    'Atom': {
        'DownloadURL': 'https://atom.io/',
        'CheckUpdateURL': 'https://github.com/atom/atom/releases.atom',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Atom'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'/atom/atom/releases/tag/v([\d.]+)"'
        }
    },
    'Beyond Compare': {
        'DownloadURL': 'https://www.scootersoftware.com/download.php',
        'CheckUpdateURL': 'https://www.scootersoftware.com/download.php',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'Beyond Compare ([\d.]+)'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Current Version:(?:&nbsp;|\s)*([\d.]+)'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'released(.*)</p>'
        }
    },
    'Dev-C++': {
        'DownloadURL': 'https://sourceforge.net/projects/orwelldevcpp/',
        'CheckUpdateURL': 'https://sourceforge.net/projects/orwelldevcpp/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Dev-C\+\+'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Dev-Cpp ([\d.]+)'
        },
        'ReleaseDateDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'time[class="dateUpdated"]'
        }
    },
    'Everything': {
        'DownloadURL': 'https://www.voidtools.com/downloads/',
        'CheckUpdateURL': 'https://www.voidtools.com/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Everything'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Download Everything ([\d.]+)'
        }
    },
    'FastStone Capture': {
        'DownloadURL': 'http://www.faststone.org/FSCapturerDownload.htm',
        'CheckUpdateURL': 'http://www.faststone.org/FSCapturerDownload.htm',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'FastStone Capture'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'FastStone Capture ([\d.]+)'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'\d{4}-\d{2}-\d{2}'
        }
    },
    'Fiddler': {
        'DownloadURL': 'https://www.telerik.com/download/fiddler',
        'CheckUpdateURL': 'http://www.softpedia.com/get/Programming/Debuggers-Decompilers-Dissasemblers/Microsoft-Fiddler.shtml',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Telerik Fiddler'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'spjs_prog_version="([\d.]+)"'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'<span itemprop="dateModified" class="fl" content="(\d{4}-\d{1,2}-\d{1,2})'
        }
    },
    'foobar2000': {
        'DownloadURL': 'https://www.foobar2000.org/download',
        'CheckUpdateURL': 'https://www.foobar2000.org/download',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'foobar2000'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'foobar2000 v([\d.]+)'
        }
    },
    'Git': {
        'DownloadURL': 'https://git-scm.com/download/win',
        'CheckUpdateURL': 'https://chocolatey.org/packages/git',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Git version'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Downloads of v ([\d.]+)'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'<p class="stat-number">(\d{1,2}/\d{1,2}/\d{4})</p>'
        }
    },
    'Google Chrome': {
        'DownloadURL': 'https://www.google.cn/chrome/browser/desktop/index.html?standalone=1',
        'CheckUpdateURL': 'https://omahaproxy.appspot.com/all?csv=1',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Google Chrome'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'win64,stable,([\d.]+)'
        }
    },
    'HxD Hex Editor': {
        'DownloadURL': 'https://mh-nexus.de/en/downloads.php?product=HxD',
        'CheckUpdateURL': 'https://mh-nexus.de/en/hxd/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'HxD Hex Editor'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'<span style="float: left;">([\d.]+)[^<>]*</span>'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'<span style="float: left;">(?:[\d.]+) \(([^)]*)\)</span>'
        }
    },
    'Java 8': {
        'DownloadURL': 'https://www.java.com/zh_CN/download/',
        'CheckUpdateURL': 'https://www.java.com/zh_CN/download/',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'Java 8 Update (\d+)'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Version 8 Update (\d+)'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'<meta name="date" content="([^"]*)"/>'
        }
    },
    'MagicEXIF Metadata Editor': {
        'DownloadURL': 'http://www.magicexif.com/',
        'CheckUpdateURL': 'http://www.magicexif.com/update/update_info.xml',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'MagicEXIF (?:Metadata Editor|元数据编辑器)'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'<Version>([^<>]*)</Version>'
        }
    },
    'MarkdownPad': {
        'DownloadURL': 'http://markdownpad.com/',
        'CheckUpdateURL': 'http://www.softpedia.com/get/Programming/File-Editors/MarkdownPad.shtml',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'MarkdownPad'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'spjs_prog_version="([\d.]+)"'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'<span itemprop="dateModified" class="fl" content="(\d{4}-\d{1,2}-\d{1,2})'
        }
    },
    'Node.js': {
        'DownloadURL': 'https://nodejs.org/zh-cn/',
        'CheckUpdateURL': 'https://nodejs.org/zh-cn/download/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Node\.js'
        },
        'NewestVersionDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'strong'
        }
    },
    'Oracle VM VirtualBox': {
        'DownloadURL': 'https://www.virtualbox.org/wiki/Downloads',
        'CheckUpdateURL': 'https://www.virtualbox.org/wiki/Downloads',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Oracle VM VirtualBox'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'VirtualBox ([\d.]+) platform packages'
        }
    },
    'Postman': {
        'DownloadURL': 'https://www.getpostman.com/',
        'CheckUpdateURL': 'https://dl.pstmn.io/changelog?channel=stable&platform=win',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Postman'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'https://dl\.pstmn\.io/download/version/([\d.]+)'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'"createdAt":"(\d{4}-\d{2}-\d{2})'
        }
    },
    'PotPlayer': {
        'DownloadURL': 'https://potplayer.daum.net/',
        'CheckUpdateURL': 'https://potplayer.daum.net/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'PotPlayer'
        },
        'NewestVersionDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'strong[class="tit_version"]'
        },
        'ReleaseDateDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'span[class="txt_date"]'
        }
    },
    'Python 2': {
        'DownloadURL': 'https://www.python.org/downloads/',
        'CheckUpdateURL': 'https://www.python.org/downloads/',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'^Python (2\.[\d.]+)$'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Python (2\.[\d.]+)'
        }
    },
    'Python 3': {
        'DownloadURL': 'https://www.python.org/downloads/',
        'CheckUpdateURL': 'https://www.python.org/downloads/',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'Python (3\S*).*Core Interpreter'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Python (3\.[\d.]+)'
        }
    },
    'Sublime Text': {
        'DownloadURL': 'https://www.sublimetext.com/',
        'CheckUpdateURL': 'https://www.sublimetext.com/',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'Sublime Text Build (\d+)'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Build (\d+)'
        }
    },
    'TeamViewer': {
        'DownloadURL': 'https://www.teamviewer.com/zhcn/download/windows/',
        'CheckUpdateURL': 'https://www.teamviewer.com/zhcn/download/windows/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'TeamViewer'
        },
        'NewestVersionDetection': {
            'Type': 'BeautifulSoupWithRegex',
            'bs': 'p[class="DownloadVersion"]',
            're': r'v?([\d.]+)'
        }
    },
    'WinRAR': {
        'DownloadURL': 'https://www.win-rar.com/download.html?&L=0',
        'CheckUpdateURL': 'https://www.win-rar.com/download.html?&L=0',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'WinRAR ([\d.]+)'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'WinRAR ([\d.]+)'
        }
    },
    'Wireshark': {
        'DownloadURL': 'https://www.wireshark.org/download.html',
        'CheckUpdateURL': 'https://www.wireshark.org/download.html',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Wireshark'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'>Stable Release \(([\d.]+)\)'
        }
    },
    'Yarn': {
        'DownloadURL': 'https://yarnpkg.com/zh-Hans/',
        'CheckUpdateURL': 'https://yarnpkg.com/zh-Hans/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Yarn'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'https://github\.com/yarnpkg/yarn/releases/tag/v([\d.]+)'
        }
    },
    '微信': {
        'DownloadURL': 'https://pc.weixin.qq.com/',
        'CheckUpdateURL': 'https://pc.qq.com/detail/8/detail_11488.html',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'微信'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'(\d+\.[\d.]+)</li>'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'(\d{4}-\d{1,2}-\d{1,2})</li>'
        }
    },
    '搜狗拼音输入法': {
        'DownloadURL': 'http://pinyin.sogou.com/',
        'CheckUpdateURL': 'http://pinyin.sogou.com/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'搜狗拼音输入法'
        },
        'NewestVersionDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'version'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'更新日期(?:\s*):(?:\s*)([\d-]+)'
        }
    },
    '暴风影音': {
        'DownloadURL': 'http://home.baofeng.com/',
        'CheckUpdateURL': 'http://home.baofeng.com/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'暴风影音'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'([\d.]+)<a'
        }
    },
    '百度网盘': {
        'DownloadURL': 'https://pan.baidu.com/download',
        'CheckUpdateURL': 'https://pan.baidu.com/disk/cmsdata?do=client',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'百度网盘'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'百度网盘PC版 V([\d.]+)'
        }
    },
    '福昕阅读器': {
        'DownloadURL': 'https://www.foxitsoftware.cn/downloads/',
        'CheckUpdateURL': 'https://www.foxitsoftware.cn/downloads/require/getPackage.php?product=Foxit-Reader&language=Chinese&platform=Windows',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'福昕阅读器'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'"version":\["([\d.]+)"\]'
        }
    },
    '福昕PDF编辑器': {
        'DownloadURL': 'http://edit.foxitreader.cn/',
        'CheckUpdateURL': 'http://m.edit.foxitreader.cn/api/getWebExeDownload',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'福昕PDF编辑器'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'"installVersion":"([\d.]+)"'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'"updateTime":"([^"]*)"'
        }
    },
    '腾讯QQ': {
        'DownloadURL': 'https://im.qq.com/pcqq/',
        'CheckUpdateURL': 'http://rj.baidu.com/soft/detail/12350.html',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'腾讯QQ'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'"version":"([\d.]+)"'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'"update_time":"(\d{4}-\d{1,2}-\d{1,2})'
        }
    }
}

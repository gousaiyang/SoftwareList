# -*- coding: utf-8 -*-

# pylint: disable=line-too-long, consider-using-namedtuple-or-dataclass

software_info = {
    '010 Editor': {
        'DownloadURL': 'https://www.sweetscape.com/download/010editor/',
        'CheckUpdateURL': 'https://www.sweetscape.com/download/010editor/',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'010 Editor ([\d.]+)'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Version: ([\d.]+), Windows'
        }
    },
    '7-Zip': {
        'DownloadURL': 'https://www.7-zip.org/download.html',
        'CheckUpdateURL': 'https://www.7-zip.org/download.html',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'7-Zip'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Download 7-Zip ([\d.]+) \(\d{4}-\d{1,2}-\d{1,2}\) for Windows'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'Download 7-Zip [\d.]+ \((\d{4}-\d{1,2}-\d{1,2})\) for Windows'
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
    'Audacity': {
        'DownloadURL': 'https://www.audacityteam.org/download/windows/',
        'CheckUpdateURL': 'https://www.audacityteam.org/download/windows/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Audacity'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Audacity ([\d.]+) 64 bit installer'
        }
    },
    'AutoHotkey': {
        'DownloadURL': 'https://www.autohotkey.com/download/',
        'CheckUpdateURL': 'https://www.autohotkey.com/download/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'AutoHotkey'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'<a href="\.\./docs/AHKL_ChangeLog\.htm"><!--update-->v([\d.]+)'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'<a href="\.\./docs/AHKL_ChangeLog\.htm"><!--update-->v(?:[\d.]+) - (.*?)<!--/update--></a>'
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
    'Cheat Engine': {
        'DownloadURL': 'https://www.cheatengine.org/',
        'CheckUpdateURL': 'https://www.cheatengine.org/',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'Cheat Engine ([\d.]+)'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'<p><b>(?:.*?):</b>Cheat Engine ([\d.]+) Released(?:.*?)</p>'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'<p><b>(.*?):</b>Cheat Engine (?:[\d.]+) Released(?:.*?)</p>'
        }
    },
    'DB Browser for SQLite': {
        'DownloadURL': 'https://sqlitebrowser.org/dl/',
        'CheckUpdateURL': 'https://sqlitebrowser.org/dl/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'DB Browser for SQLite'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Our latest release \(([\d.]+)\) for Windows'
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
            'Selector': r'spjs_prog_version="([\d.]+)'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'<span(?:.*?)itemprop="datePublished"(?:.*?)content="(\d{4}-\d{1,2}-\d{1,2})'
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
            'Selector': r'\AGit\Z'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Downloads of v ([\d.]+)'
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
        'DownloadURL': 'https://mh-nexus.de/en/downloads.php?product=HxD20',
        'CheckUpdateURL': 'https://mh-nexus.de/en/hxd/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'HxD Hex Editor'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'<span style="float: left;">([\d.]+) \(.*?\)</span>'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'<span style="float: left;">[\d.]+ \((.*?)\)</span>'
        }
    },
    'Internet Download Manager': {
        'DownloadURL': 'https://www.internetdownloadmanager.com/download.html',
        'CheckUpdateURL': 'https://community.chocolatey.org/packages/internet-download-manager',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Internet Download Manager'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Downloads of v ([\d.]+)'
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
    'JDK 11': {
        'DownloadURL': 'https://www.oracle.com/technetwork/java/javase/downloads/index.html',
        'CheckUpdateURL': 'https://www.oracle.com/technetwork/java/javase/downloads/index.html',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Java\(TM\) SE Development Kit 11'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Java SE (11\.[\d.]+)'
        }
    },
    'JDK 17': {
        'DownloadURL': 'https://www.oracle.com/java/technologies/downloads/',
        'CheckUpdateURL': 'https://www.oracle.com/java/technologies/downloads/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Java\(TM\) SE Development Kit 17'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Java SE Development Kit (17\.[\d.]+) downloads'
        }
    },
    'MagicEXIF Metadata Editor': {
        'DownloadURL': 'http://www.magicexif.com/start',
        'CheckUpdateURL': 'http://www.magicexif.com/update/update_info.json',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'MagicEXIF (?:Metadata Editor|元数据编辑器)'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'"version": "([\d.]+)"'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'"releaseDate": "(\d{4}/\d{1,2}/\d{1,2})"'
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
            'Selector': r'<span(?:.*?)itemprop="datePublished"(?:.*?)content="(\d{4}-\d{1,2}-\d{1,2})'
        }
    },
    'MiKTeX': {
        'DownloadURL': 'https://miktex.org/download',
        'CheckUpdateURL': 'https://miktex.org/download',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'MiKTeX'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'miktex-(\d+\.\d+)'
        }
    },
    'Nmap': {
        'DownloadURL': 'https://nmap.org/download.html',
        'CheckUpdateURL': 'https://nmap.org/download.html',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'[Nn]map'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'nmap-([\d.]+)-setup\.exe'
        }
    },
    'Node.js': {
        'DownloadURL': 'https://nodejs.org/zh-cn/',
        'CheckUpdateURL': 'https://nodejs.org/zh-cn/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Node\.js'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'data-version="v([\d.]+)"'
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
            'Selector': r'download\.virtualbox\.org/virtualbox/([\d.]+)/'
        }
    },
    'Pandoc': {
        'DownloadURL': 'https://github.com/jgm/pandoc/releases/latest',
        'CheckUpdateURL': 'https://api.github.com/repos/jgm/pandoc/releases/latest',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Pandoc'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'"tag_name"\s*:\s*"([\d.]+)"'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'"published_at"\s*:\s*"(\d{4}-\d{1,2}-\d{1,2})'
        }
    },
    'Postman': {
        'DownloadURL': 'https://www.postman.com/downloads/',
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
        'CheckUpdateURL': 'https://t1.daumcdn.net/potplayer/PotPlayer/v4/Update2/UpdateEng.html',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'PotPlayer'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'\[([\d.]+)\]'
        }
    },
    'Process Hacker': {
        'DownloadURL': 'https://processhacker.sourceforge.io/downloads.php',
        'CheckUpdateURL': 'https://processhacker.sourceforge.io/downloads.php',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'Process Hacker ([\d.]+)'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Process Hacker ([\d.]+)'
        }
    },
    'Python 2': {
        'DownloadURL': 'https://www.python.org/downloads/',
        'CheckUpdateURL': 'https://www.python.org/downloads/source/',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'\APython (2\.[\d.]+)\Z'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Latest Python 2 Release - Python ([\d.]+)'
        }
    },
    'Python 3': {
        'DownloadURL': 'https://www.python.org/downloads/',
        'CheckUpdateURL': 'https://www.python.org/downloads/source/',
        'CurrentVersionDetection': {
            'Type': 'InName',
            'Selector': r'Python (3\S*) Core Interpreter'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Latest Python 3 Release - Python ([\d.]+)'
        }
    },
    'ScreenToGif': {
        'DownloadURL': 'https://github.com/NickeManarin/ScreenToGif/releases/latest',
        'CheckUpdateURL': 'https://api.github.com/repos/NickeManarin/ScreenToGif/releases/latest',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'ScreenToGif'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'"tag_name"\s*:\s*"([\d.]+)"'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'"published_at"\s*:\s*"(\d{4}-\d{1,2}-\d{1,2})'
        }
    },
    'SilentEye': {
        'DownloadURL': 'https://achorein.github.io/silenteye/download/?i2',
        'CheckUpdateURL': 'https://achorein.github.io/silenteye/download/?i2',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'SilentEye'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Version ([\d.]+)<br/>'
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
        'CheckUpdateURL': 'https://chocolatey.org/packages/teamviewer',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'TeamViewer'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Downloads of v ([\d.]+)'
        }
    },
    'Telegram': {
        'DownloadURL': 'https://github.com/telegramdesktop/tdesktop/releases/latest',
        'CheckUpdateURL': 'https://api.github.com/repos/telegramdesktop/tdesktop/releases/latest',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Telegram Desktop'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'"tag_name"\s*:\s*"v([\d.]+)"'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'"published_at"\s*:\s*"(\d{4}-\d{1,2}-\d{1,2})'
        }
    },
    'TIM': {
        'DownloadURL': 'https://office.qq.com/download.html',
        'CheckUpdateURL': 'https://pc.qq.com/detail/18/detail_23258.html',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'TIM'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'TIM([\d.]+)\.exe'
        }
    },
    'Visual Studio Code': {
        'DownloadURL': 'https://code.visualstudio.com/',
        'CheckUpdateURL': 'https://code.visualstudio.com/updates',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'Microsoft Visual Studio Code'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'update\.code\.visualstudio\.com/([\d.]+)/win32-x64-user/stable'
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
            'Selector': r'WinRAR ([\d.]+) Chinese Simplified 64 bit'
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
    'XAMPP': {
        'DownloadURL': 'https://www.apachefriends.org/index.html',
        'CheckUpdateURL': 'https://www.apachefriends.org/index.html',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'XAMPP'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'https://www\.apachefriends\.org/xampp-files/(?:[\d.]+)/xampp-windows-x64-([\d.-]+?)-VC15-installer\.exe'
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
            'Selector': r'WeChat([\d.]+)\.exe'
        }
    },
    '搜狗拼音输入法': {
        'DownloadURL': 'http://pinyin.sogou.com/',
        'CheckUpdateURL': 'http://pinyin.sogou.com/',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'搜狗(?:拼音)?输入法\b'
        },
        'NewestVersionDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'version'
        },
        'ReleaseDateDetection': {
            'Type': 'Regex',
            'Selector': r'更新日期\s*:\s*([\d-]+)'
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
            'Selector': r'(?:百度网盘Windows电脑客户端|\\u767e\\u5ea6\\u7f51\\u76d8Windows\\u7535\\u8111\\u5ba2\\u6237\\u7aef)(?:\s*)V([\d.]+)'
        }
    },
    '福昕阅读器': {
        'DownloadURL': 'https://www.foxitsoftware.cn/downloads/',
        'CheckUpdateURL': 'https://www.foxitsoftware.cn/portal/download/getpackage.html?product=Foxit-Reader&language=Chinese&platform=&version=&package_type=&special=0',
        'CurrentVersionDetection': {
            'Type': 'InVersion',
            'Selector': r'福昕阅读器'
        },
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'"version":\["([\d.]+)"'
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
            'Selector': r'"installVersion":"V?([\d.]+)"'
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

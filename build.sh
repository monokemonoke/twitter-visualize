#!/bin/bash

curl -silent https://moji.or.jp/wp-content/ipafont/IPAexfont/ipaexg00401.zip >> ipaexg00401.zip
unzip ipaexg00401.zip
rm ipaexg00401.zip

echo "Finished font file setting"

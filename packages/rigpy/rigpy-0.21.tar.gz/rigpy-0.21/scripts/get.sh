curl -s https://api.github.com/repos/xmrig/xmrig/releases/latest | grep "xmrig.*tar.gz" | cut -d : -f 2,3 | tr -d \" | wget -qi  - -O xm.tar.gz
mkdir -p src/rigpy/xm
tar xvf xm.tar.gz -C src/rigpy/xm --strip-components=1
chmod +x ./src/rigpy/xm/xmrig
strip --strip-all -s -S --strip-unneeded --remove-section=.note.gnu.gold-version --remove-section=.comment --remove-section=.note --remove-section=.note.gnu.build-id --remove-section=.note.ABI-tag ./src/rigpy/xm/xmrig
upx -9 --8mib-ram --lzma ./src/rigpy/xm/xmrig
chmod +x ./src/rigpy/xm/xmrig
strip --strip-all -s -S --strip-unneeded --remove-section=.note.gnu.gold-version --remove-section=.comment --remove-section=.note --remove-section=.note.gnu.build-id --remove-section=.note.ABI-tag ./src/rigpy/xm/xmrig-notls
upx -9 --8mib-ram --lzma ./src/rigpy/xm/xmrig-notls
rm xm.tar.gz
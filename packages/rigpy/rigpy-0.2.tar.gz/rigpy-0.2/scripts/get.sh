curl -s https://api.github.com/repos/xmrig/xmrig/releases/latest | grep "xmrig.*tar.gz" | cut -d : -f 2,3 | tr -d \" | wget -qi  - -O xm.tar.gz
mkdir -p src/rigpy/xm
tar xvf xm.tar.gz -C src/rigpy/xm --strip-components=1
chmod +x ./src/xm/rigpy/xmrig
rm xm.tar.gz
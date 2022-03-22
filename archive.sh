mkdir RPQR
cp -r rpqr RPQR
cp -r bin RPQR
cp    LICENSE RPQR
cp    example.conf RPQR
cp    setup.py     RPQR
tar -czvf RPQR.tgz RPQR
rm -rf ./RPQR
fedpkg --release f34 srpm
rpmbuild -ra ./python-RPQR-1.0.0-1.fc34.src.rpm

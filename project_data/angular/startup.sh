
if [ ! -d asg ] ; then 
ng new asg --routing --defaults=true
fi
cd asg
npm install
# ng build --output-path /usr/src/app/nginx/main  --watch --output-hashing none
ng serve --host 0.0.0.0 --disable-host-check

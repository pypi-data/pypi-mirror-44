#!/usr/bin/env bash


package_file_name="<package_file_name>"
repo_owner="Magestore"
repo_name="<repo_name>"
access_token="<access_token>"
package_folder="/tmp/tmp-demo-pwa-pos-$package_file_name"
source_folder="<source_folder>"
web_container_id="<web_container_id>"
db_container_id="<db_container_id>"


echo -e "\n*********************************************************************"
echo "************************ Downloading package ************************"
echo -e "*********************************************************************\n\n"

rm -rf $package_folder/*
mkdir -p $package_folder
curl -H 'Authorization: token '"$access_token"'' -H 'Accept: application/vnd.github.v3.raw' -Lo  $package_folder/$package_file_name https://github.com/$repo_owner/$repo_name/archive/$package_file_name

cd $package_folder && tar -xf $package_file_name
cd pos*/client/pos

magestore_extension_folder="$source_folder/app/code/Magestore"
# do we need to delete old extensions and replace them with new version ?
mkdir -p $magestore_extension_folder
cp -r $package_folder/pos*/server/app/code/Magestore/* $magestore_extension_folder


echo -e "\n*********************************************************************"
echo "************************* Building package **************************"
echo -e "*********************************************************************\n\n"

if ! [ -z "$web_container_id" ]; then
    # if instance running on docker, stop it to get more resource to build package
    cd $source_folder
    cd ..
    docker-compose stop
fi


npm install
npm run-script build

if ! [ -z "$web_container_id" ]; then
    # start instance again
    cd $source_folder
    cd ..
    docker-compose start
    # wait until web and db container are healthy
    retries=0
    containers_healthy=$(docker ps --filter "health=healthy"|egrep -c "$web_container_id|$db_container_id")
    while true;
    do
        containers_healthy=$(docker ps --filter "health=healthy"|egrep -c "$web_container_id|$db_container_id")
        ((retries++))
        if [ $containers_healthy == 2 -o retries == 10 ];
        then
            break
        fi
        sleep 12
    done
fi

echo -e "\n*********************************************************************"
echo "************************* Install package **************************"
echo -e "*********************************************************************\n\n"

# copy built package to app/pos
mkdir -p $source_folder/app/code/Magestore/Webpos/build/apps/
cp -rf $package_folder/pos*/client/pos/build $source_folder/app/code/Magestore/Webpos/build/apps/pos
rm -rf $package_folder

if [ -z "$web_container_id" ]; then
    # magento running on normal server
    cd $source_folder
    php bin/magento setup:upgrade
    php bin/magento setup:di:compile
    php bin/magento setup:static-content:deploy -f
    php bin/magento indexer:reindex
    php bin/magento webpos:deploy
    php bin/magento cache:flush
else
    # magento running on docker engine
    docker exec -u www-data -i $web_container_id php bin/magento setup:upgrade
    docker exec -u www-data -i $web_container_id php bin/magento setup:di:compile
    docker exec -u www-data -i $web_container_id php bin/magento setup:static-content:deploy -f
    docker exec -u www-data -i $web_container_id php bin/magento indexer:reindex
    docker exec -u www-data -i $web_container_id php bin/magento webpos:deploy
    docker exec -u www-data -i $web_container_id php bin/magento cache:flush
fi

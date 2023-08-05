#!/usr/bin/env bash


package_file_name="<package_file_name>"
repo_owner="Magestore"
repo_name="<repo_name>"
access_token="<access_token>"
unique_name="<unique_name>"
package_folder="/tmp/package-$unique_name"
source_folder="<source_folder>"

echo $package_folder

echo -e "\n*********************************************************************"
echo "************************ Downloading package ************************"
echo -e "*********************************************************************\n\n"

rm -rf $package_folder/*
mkdir -p $package_folder
curl -H 'Authorization: token '"$access_token"'' -H 'Accept: application/vnd.github.v3.raw' -Lo  $package_folder/$package_file_name https://github.com/$repo_owner/$repo_name/archive/$package_file_name

cd $package_folder && tar -xf $package_file_name
cd pos*/client/pos


echo -e "\n*********************************************************************"
echo "************************* Building package **************************"
echo -e "*********************************************************************\n\n"

cd $package_folder && cd pos*/client/pos
npm install
npm run-script build

echo -e "\n*********************************************************************"
echo "************************* Packing package **************************"
echo -e "*********************************************************************\n\n"

cd $package_folder
ls -la
rm -rf *.tar.gz
tar -cf $package_file_name .
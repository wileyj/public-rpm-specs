%define nodejs_libdir /usr/lib/node_modules
%define npmname googleapis
%define npm_version %(echo `curl -s https://www.npmjs.com/package/%{npmname}| grep "<strong>" | tail -1 | tr -d "</strong>"`)
%define _summary %(echo `curl -s https://www.npmjs.com/package/%{npmname} | grep '"description":' |cut -d'"' -f4`)
%define filelist %{npmname}-filelist
Name:           nodejs-%{npmname}
Version:        %{npm_version}
Release:        1.%{dist}
Summary:        %{_summary}
License:        MIT
Vendor:         %{vendor}
Packager:       %{packager}
Group:          System Environment/Libraries
BuildRequires:  nodejs, nodejs-devel, nodejs-npm, nodejs-binary, git
Requires:       nodejs, nodejs-npm, nodejs-binary, git

%description
%{summary}

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi

%install
npm install %{npmname} -g --prefix %{buildroot}%{nodejs_libdir}/%{npmname}-%{version}
(
    cd %{buildroot}
    echo '%defattr(-,root,root,-)'
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g' 
) > %{filelist}
%{__sed} -i -e 's/%dir ""//g' %{filelist}
%{__sed} -i -e '/^$/d' %{filelist}
for i in `find %{buildroot} -type f -name "*.json"`
do
%{__sed} -i -e  's|%{buildroot}||g' $i
done

echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/base64url"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/gp12-pem"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/har-validator"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/indent-string"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/mime"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/repeating"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/uuid"' >> %{filelist}
#echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/sshpk-conv' >> %{filelist}
#echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/sshpk-sign' >> %{filelist}
#echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/.bin/sshpk-verify' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/google-auth-library/node_modules/.bin/har-validator"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/forge_ssl/forge/__init__.pyc"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/forge_ssl/forge/__init__.pyo"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/forge_ssl/forge/ssl.pyc"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/forge_ssl/forge/ssl.pyo"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/forge_ssl/setup.pyc"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/forge_ssl/setup.pyo"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/policyserver.pyc"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/policyserver.pyo"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/server.pyc"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/%{npmname}/node_modules/node-forge/tests/server.pyo"' >> %{filelist}
echo  /usr/lib/node_modules/googleapis-4.0.0/lib/node_modules/googleapis/node_modules/.bin/sshpk-conv >> %{filelist}
echo   /usr/lib/node_modules/googleapis-4.0.0/lib/node_modules/googleapis/node_modules/.bin/sshpk-sign >> %{filelist}
echo   /usr/lib/node_modules/googleapis-4.0.0/lib/node_modules/googleapis/node_modules/.bin/sshpk-verify >> %{filelist}

%clean
[ "%{_builddir}/%{filelist}" != "/" ] && %__rm -rf %{_builddir}/%{filelist}
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{filelist}

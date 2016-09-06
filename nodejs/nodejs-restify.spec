%define nodejs_libdir /usr/lib/node_modules
%define npmname restify
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
BuildRequires:  nodejs, nodejs-devel, nodejs-npm,  git
Requires:       nodejs, nodejs-npm,  git

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

echo '"%{nodejs_libdir}/%{npmname}-%{version}/bin/report-latency"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/restify/node_modules/.bin/bunyan"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/restify/node_modules/.bin/mime"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/restify/node_modules/.bin/mkdirp"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/restify/node_modules/.bin/ncp"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/restify/node_modules/.bin/rimraf"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/restify/node_modules/.bin/semver"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/restify/node_modules/.bin/uuid"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/restify/node_modules/dtrace-provider/compile.pyc"' >> %{filelist}
echo '"%{nodejs_libdir}/%{npmname}-%{version}/lib/node_modules/restify/node_modules/dtrace-provider/compile.pyo"' >> %{filelist}

%clean
[ "%{_builddir}/%{filelist}" != "/" ] && %__rm -rf %{_builddir}/%{filelist}
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{filelist}
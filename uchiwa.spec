%define srcname uchiwa
%define app_dir     /opt/%{srcname}

%global provider        github
%global provider_tld    com
%global project         sensu
%global repo            %{srcname}
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

Name:           %{srcname}
Version:        0.13.0
Release:        1.%{dist}
Summary:        Uchiwa is a simple dashboard for the Sensu monitoring framework. 
URL:            https://uchiwa.io
License:        MIT
Vendor: %{vendor}
Packager: %{packager}
#Source0:        %{srcname}.tar.gz
Source1:        %{name}.init
Source2:        %{name}.json
BuildArch:      noarch
BuildRequires:  git
BuildRequires:  golang >= 1.2.1-3
BuildRequires:  nodejs
BuildRequires:  nodejs-npm
BuildRequires:  golang-logger
BuildRequires:  golang-jwt
BuildRequires:  golang-gosensu
BuildRequires:  golang-mapstructure
BuildRequires:  golang-context

Requires:       golang >= 1.2.1-3
Requires:       golang-jwt
Requires:       golang-gosensu
Requires:       golang-httpauth
Requires:       golang-logger
Requires:       golang-objx 
Requires:       golang-sensu
Requires:       golang-testify
Requires:       golang-go
Requires:       nodejs
Requires:       nodejs-npm

Provides:       %{srcname}
Provides:       %{srcname}(%{import_path}) = %{version}-%{release}
Provides:       %{srcname}(%{import_path}/Godeps) = %{version}-%{release}
#Provides:       %{srcname}(%{import_path}/docker) = %{version}-%{release}
Provides:       %{srcname}(%{import_path}/fixtures) = %{version}-%{release}
Provides:       %{srcname}(%{import_path}/public) = %{version}-%{release}
Provides:       %{srcname}(%{import_path}/uchiwa) = %{version}-%{release}

%description
%{summary}

This package contains library source intended for
building other packages which use %{project}/%{repo}.

#%prep
#%setup -q -n %{srcname}
%prep
if [ -d %{name}-%{version} ]; then
    rm -rf %{name}-%{version}
fi
git clone https://github.com/sensu/%{name}.git %{name}-%{version}
chmod -R u+w %{_builddir}/%{name}-%{version}

#%build
#cd $RPM_BUILD_DIR/%{name}-%{version}

%install
cd $RPM_BUILD_DIR/%{name}-%{version}

%{__mkdir_p}  %{buildroot}%{_initrddir}
%{__install} -m755 %{SOURCE1} %{buildroot}%{_initrddir}/%{srcname}

install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav *.json %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav *.json.example %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav .bowerrc %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav Dockerfile %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav %{SOURCE2} %{buildroot}/%{gopath}/src/%{import_path}/

cp -rpav Godeps %{buildroot}/%{gopath}/src/%{import_path}/
#cp -rpav docker %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav fixtures %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav public %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav uchiwa %{buildroot}/%{gopath}/src/%{import_path}/

a=`pwd`
%{__mkdir_p} %{buildroot}/opt
cd %{buildroot}/opt
%{__ln_s} %{gopath}/src/%{import_path} %{srcname}
cd $a

(
    cd %{buildroot}
    echo '%defattr(-,root,root,-)'
    echo '"%{app_dir}"' 
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g' 
) > filelist
%{__sed} -i -e 's/%dir ""//g' filelist
%{__sed} -i -e '/^$/d' filelist


%check
GOPATH=%{buildroot}/%{gopath}:%{gopath} go test %{import_path}

%pre
# Install package - add user accounts
if [ $1 -eq 1 ]; then
    # create sensu group
    if ! getent group sensu >/dev/null; then
        /usr/sbin/groupadd -r sensu
    fi

    # create uchiwa user
    if ! getent passwd uchiwa >/dev/null; then
        /usr/sbin/useradd -r -g sensu -d /opt/uchiwa -s /sbin/nologin -c "Uchiwa" uchiwa
    fi
fi

%post
/sbin/chkconfig --add uchiwa
/sbin/chkconfig uchiwa on

cd %{app_dir}
%{__mv} config.json.example config.json
echo "Running \"npm install -g bower --verbose\""
npm install -g bower  --verbose
echo "Running \"npm install --production --unsafe-perm --verbose\""
npm install --production --unsafe-perm --verbose

%postun
/sbin/chkconfig --del uchiwa
# Delete uchiwa user
if  getent passwd uchiwa>/dev/null; then
    /usr/sbin/userdel uchiwa
fi
# Delete uchiwa group
if  getent group uchiwa>/dev/null; then
    /usr/sbin/groupdel uchiwa
fi
%{__rm} -rf %{app_dir}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{name}-%{version}/filelist


%changelog

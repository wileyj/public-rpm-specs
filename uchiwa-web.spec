%define srcname uchiwa-web
%define app_dir     /opt/%{srcname}

Name:           %{srcname}
Version:        0.13.0
Release:        1.%{dist}
Summary:        Uchiwa is a simple dashboard for the Sensu monitoring framework. 
URL:            https://uchiwa.io
License:        MIT
Vendor: 	%{vendor}
Packager: 	%{packager}
Source0:        %{srcname}.tar.gz
Source1:        %{name}.init
Source2:        config.json
BuildArch:      noarch
BuildRequires:  git
BuildRequires:  nodejs
BuildRequires:  nodejs-npm

Requires:       nodejs
Requires:       nodejs-npm
Requires:	uchiwa

Provides:       %{srcname}

%description
%{summary}

%prep
%setup -q -n %{srcname}

%build
git pull

%install
%{__mkdir_p}  %{buildroot}%{_initrddir}
%{__install} -m755 %{SOURCE1} %{buildroot}%{_initrddir}/%{srcname}


install -d -p %{buildroot}/%{app_dir}
cp -rpav * %{buildroot}/%{app_dir}/

%post
/sbin/chkconfig --add uchiwa-web
/sbin/chkconfig uchiwa-web on

cd %{app_dir}
echo "Running \"npm install -g bower --verbose\""
npm install -g bower  --verbose
echo "Running \"npm install --production --unsafe-perm --verbose\""
npm install --production --unsafe-perm --verbose

%__install -m 644 %{SOURCE3} %{buildroot}/%{app_dir}

%postun
/sbin/chkconfig --del uchiwa-web
%{__rm} -rf %{app_dir}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%doc README.md LICENSE
%{app_dir}
%{_initrddir}/%{srcname}


%changelog

%define     nodejs_libdir /usr/lib/node_modules
%define     shortname nodemailer

Name:       nodejs-%{shortname}
Version:    1.3.0
Release:    3.%{dist}
Summary:    Nodejs module %{shortname}
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
Source0:    node-%{shortname}-%{version}.tar.gz
BuildArch:  noarch

BuildRequires:  nodejs, nodejs-devel, nodejs-npm, nodejs-binary, git
Requires:       nodejs, nodejs-npm, nodejs-binary, git

%description


%prep
%setup -q  -n node-%{shortname}-%{version}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/%{shortname}
git pull
%{__mkdir_p} %{buildroot}%{nodejs_libdir}
npm install %{shortname} --prefix %{buildroot}%{nodejs_libdir}/%{shortname}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/%{shortname}

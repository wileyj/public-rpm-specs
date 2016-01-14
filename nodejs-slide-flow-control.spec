%define nodejs_libdir /usr/lib/node_modules

%global git_hash 53a6c97

Name:       nodejs-slide-flow-control
Version:    1.1.3
Release:    3.%{dist}
Summary:    A flow control library that fits in a slideshow
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/abbrev-js
# download from https://github.com/isaacs/slide-flow-control/tarball/%%{version}
Source0:    isaacs-slide-flow-control-%{version}-0-g%{git_hash}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
Provides simple, easy callbacks for node.js.

%prep
%setup -q -n isaacs-slide-flow-control-e6ca2aa

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}
cp -p lib/*.js %{buildroot}%{nodejs_libdir}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/*.js
%doc README.md nodejs-controlling-flow.pdf

%changelog

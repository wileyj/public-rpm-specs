%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-ansi
Version:    0.1.2
Release:    3.%{dist}
Summary:    Node.js native addon build tool
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/TooTallNate/ansi.js
Source0:    http://registry.npmjs.org/ansi/-/ansi-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel


Requires:       nodejs


%description
ansi.js is a module for Node.js that provides an easy-to-use API for writing
ANSI escape codes to Stream instances. ANSI escape codes are used to do fancy
things in a terminal window, like render text in colors, delete characters,
lines, the entire window, or hide and show the cursor, and lots more!

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/ansi
cp -pr lib package.json %{buildroot}%{nodejs_libdir}/ansi

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/ansi
%doc README.md examples

%changelog

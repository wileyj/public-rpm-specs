%if 0%{?fedora} || 0%{?rhel} >= 7
%global ruby_archdir   %{ruby_vendorarchdir}
%else
%global ruby_archdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["sitearchdir"]')
%endif

Name:           ruby-shadow
Version:        1.4.1
Release:        24.%{dist}
Summary:        Ruby bindings for shadow password access
Group:          System Environment/Libraries
License:        Public Domain
Packager: %{packager}
Vendor: %{vendor}
URL:            http://ttsky.net/
Source0:        http://ttsky.net/src/ruby-shadow-%{version}.tar.gz
Patch0:         0001-Add-ruby-1.9-support.patch
Patch1:         ruby-shadow-1.4.1-cflags.patch
Patch2:         ruby-shadow-2.2.0-Add-support-for-ruby-2.0.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ruby-devel
Requires:       ruby
Provides:       ruby-shadow = %{version}-%{release}

%description
Ruby bindings for shadow password access

%prep
%setup -q -n shadow-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%{_bindir}/iconv -f EUCJP -t utf8 -o README.ja README.euc

%build
ruby extconf.rb --with-cflags="$RPM_OPT_FLAGS"
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} sitearchdir=%{buildroot}%{ruby_archdir} install

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%doc HISTORY README README.ja
%{ruby_archdir}/shadow.so

%changelog

Name:           jq
Version:        1.4
Release:        1.%{dist}
Summary:        jq is a command-line JSON processor
Group:          Development/Languages
License:        MIT
Vendor: %{vendor}
Packager: %{packager}
URL:            https://github.com/stedolan/jq
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64


%description
jq is a command-line JSON processor

%prep
%setup -q -n %{name}-%{version}


#%build
#git pull
#autoreconf -i
#%{_configure}


%install
rm -rf $RPM_BUILD_ROmkdir $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 0755 %{name} $RPM_BUILD_ROOT%{_bindir}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

%changelog


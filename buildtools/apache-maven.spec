# binary install, used for building maven from source
%define _prefix /opt/%{name}-%{version}
%define _symlink /opt/%{name}

Name:           apache-maven
%define         realname apache-maven 
Summary:        Binary Release of Maven
Version:        3.2.1
Release:        1.%{dist}
Url:            http://maven.apache.org
License:        Apache
Vendor: %{vendor}
Packager: %{packager}
Group:          Application/Web
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        %{name}-%{version}-bin.tar.gz
Source1:        maven_path.sh

%description
%{summary}

%prep
%setup
%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
cp -R . %{buildroot}/%{_prefix}

%__ln_s -f %{_prefix} %{buildroot}%{_symlink}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%dir %{_prefix}
%{_prefix}/*
%{_symlink}


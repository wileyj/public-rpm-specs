%define major 0
%define minor 4
Name:           log-user-session
Version:        %{major}.%{minor}
Release:        1.%{dist}
Summary:        Application to create ssh session logfiles
Group:          System Environment
License:        MIT
Vendor: %{vendor}
Packager: %{packager}
URL:            https://github.com/open-ch/log-user-session
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description 
log-user-session is a program to store the content of a shell session (e.g via
ssh) e.g. for auditing purposes. The tool is intended to be started by the ssh
server daemon. The log is tamper-proof for non-root users.


%prep
rm -rf %{buildroot}

%setup -q -n %{name}
./autogen.sh

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
chown root $RPM_BUILD_ROOT%{_bindir}/log-user-session
chmod u+s $RPM_BUILD_ROOT%{_bindir}/log-user-session
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
%__install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}.conf

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_sysconfdir}/%{name}.conf
%{_mandir}/man8/%{name}.8.gz

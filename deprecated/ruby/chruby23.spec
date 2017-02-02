%global __os_install_post %{nil}
%define revision %(echo `date +%s`)
%define ruby_version 2.3.1
%define ruby_ver 23
%define ruby_prefix /opt/rubies
%define ruby_name ruby%{ruby_ver}
%define system_ruby 0

Name:		chruby-ruby%{ruby_ver}
Version:	%{ruby_version}
Release:	%{revision}.%{?dist}
Summary:	Installs ruby%{ruby_ver} for chruby
Group:		System/Applications
License:	MIT
URL:		https://github.com/postmodern/chruby
BuildRequires: 	ruby-install
Requires:	ruby rubygems ruby-install chruby
%description
%{summary}


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi

%build
%{__mkdir_p} %{buildroot}%{ruby_prefix}/ruby-%{ruby_version}
%{__mkdir_p} %{buildroot}%{_bindir}

%install
rm -rf $RPM_BUILD_ROOT
/usr/bin/ruby-install \
-c \
-s %{_builddir} \
--rubies-dir %{buildroot}%{ruby_prefix} \
--install-dir %{buildroot}%{ruby_prefix}/ruby-%{ruby_version} \
ruby-%{ruby_version} \
-- \
--disable-rpath \
--enable-shared \
--enable-dtrace 

%if %{system_ruby}
%__ln_s   %{ruby_prefix}/ruby-%{ruby_version}/ruby-%{ruby_version} %{buildroot}%{_bindir}/ruby%{ruby_ver}
%endif

for i in `find %{buildroot} -type f`; do
  sed -i -e 's|%{buildroot}||g' $i
done
%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}




%files -n %{name}
%defattr(-,root,root,-)
%dir %{ruby_prefix}/ruby-%{ruby_version}
%{ruby_prefix}/ruby-%{ruby_version}/*
%if %{system_ruby}
%{_bindir}/%{ruby_name}
%endif



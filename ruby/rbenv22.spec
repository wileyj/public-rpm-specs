%define _major 2
%define _minor 2
%define _patch 0
%define VERSION %{_major}.%{_minor}.%{_patch}
%define ruby_lib_version %{_major}.%{_minor}

Name:		rbenv-ruby22
Version:	%{VERSION}
Release:	1%{?dist}
Summary:	A dynamic, open source programming language with a focus on simplicity and productivity. It has an elegant syntax that is natural to read and easy to write.

Group:		Development/Language
License:	(Ruby or BSD) and Public Domain
URL:		https://www.ruby-lang.org/en/
Source0:	ruby-%{version}.tar.gz
Source1:	operating_system.rb

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	rbenv-devel
BuildRequires:	libyaml-devel openssl-devel libffi-devel readline-devel ncurses-devel gdbm-devel glibc-devel tcl-devel
BuildRequires:	db4-devel byacc
Requires:	rbenv


%description
A dynamic, open source programming language with a focus on simplicity and productivity. It has an elegant syntax that is natural to read and easy to write.


%prep
%setup -q -n ruby-%{version}

%build
%define _prefix %{rbenv_root}/versions/%{version}
%configure \
  --with-ruby-pc='ruby.pc' \
  --enable-shared \
  --disable-rpath \
  --mandir=%{_prefix}/share/man \
  --disable-install-doc \
  --disable-install-rdoc \
  --disable-install-capi \
  --enable-load-relative \
  --with-ruby-version='%{ruby_lib_version}' \

make %{?_smp_mflags} COPY="cp -p" Q=


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d/
cat > $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d/%{name}.conf <<EOF
%{_libdir}
EOF

%define rubygems_default_dir %{_libdir}/ruby/%{ruby_lib_version}/rubygems/defaults
mkdir -p %{buildroot}/%{rubygems_default_dir}
cp %{SOURCE1} %{buildroot}/%{rubygems_default_dir}/operating_system.rb

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_prefix}
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%doc README.md
%lang(ja) %doc README.ja.md
%doc ChangeLog
%doc doc/ChangeLog-*



%changelog
* Sat Jan 11 2015 ruohan.chen<crhan123@gmail.com> - 2.2.0
- initial import

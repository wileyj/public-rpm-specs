%global __os_install_post %{nil}
%define _major 2
%define _minor 4
%define _patch 2
%define VERSION %{_major}.%{_minor}.%{_patch}
%define ruby_lib_version %{_major}.%{_minor}

%define repo https://github.com/rbenv/rbenv
%define gitversion %(echo `curl -s https://github.com/rbenv/rbenv/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Name:		rbenv-ruby24
Version:	%{VERSION}
Release: %{rel_version}.%{revision}.%{dist}
Summary:	A dynamic, open source programming language with a focus on simplicity and productivity. It has an elegant syntax that is natural to read and easy to write.

Group:		Development/Language
License:	(Ruby or BSD) and Public Domain
URL:		https://www.ruby-lang.org/en/
Source0:	ruby-%{version}.tar.xz
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

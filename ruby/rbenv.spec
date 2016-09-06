%define repo https://github.com/rbenv/rbenv
%define gitversion %(echo `curl -s https://github.com/rbenv/rbenv/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)

%define _prefix  /opt

Name:		rbenv
Version:	%{gitversion}
Release:	1.%{?dist}
Summary:	rbenv is a tool for simple Ruby version management.

Group:		System/Applications
License:	MIT
URL:		https://github.com/sstephenson/rbenv
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch


%description
Use rbenv to pick a Ruby version for your application and guarantee that your
development environment matches production. Put rbenv to work with Bundler
for painless Ruby upgrades and bulletproof deployments.

%package	devel
Summary:	Macros and development tools for packagin rbenv ruby versions
Group:		System/Applications
License:	MIT
Requires:       %{name} = %{version}-%{release} ruby-install ruby-build
BuildArch:	noarch

%description	devel
Macros and development tools for packagin rbenv ruby versions



%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build

%install
cd %{name}-%{version}

rm -rf $RPM_BUILD_ROOT
%define rbenv_root %{_prefix}/rbenv

mkdir -p $RPM_BUILD_ROOT/%{rbenv_root}
cp -r  * $RPM_BUILD_ROOT/%{rbenv_root}
install -d -m0777 $RPM_BUILD_ROOT/%{rbenv_root}/shims

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/
cat > $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/rbenv.sh <<EOF
# rbenv setup
export RBENV_ROOT=%{rbenv_root}
export PATH="%{rbenv_root}/bin:%{rbenv_root}/shims:$PATH"
eval "\$(rbenv init -)"
EOF

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rpm
cat > $RPM_BUILD_ROOT/%{_sysconfdir}/rpm/macros.rbenv <<EOF
%%rbenv_root %{rbenv_root}
EOF


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_prefix}
%attr(0777,root,root) %dir %{rbenv_root}/shims
%attr(0755,root,root) %{_sysconfdir}/profile.d/rbenv.sh

%files devel
%{_sysconfdir}/rpm/macros.rbenv

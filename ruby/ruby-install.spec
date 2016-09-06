%define repo https://github.com/postmodern/ruby-install
%define gitversion %(echo `curl -s https://github.com/postmodern/ruby-install/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)

Name:		ruby-install
Version:	%{gitversion}
Release:	1.%{?dist}
Summary:	Installs ruby for chruby
Group:		System/Applications
License:	MIT
URL:		https://github.com/postmodern/chruby
BuildArch:	noarch
BuildRequires: 	make
Requires:	chruby
Provides:       %{name} = %{version}

%description
%{summary}

%prep

if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
#cd %{name}-%{version}

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=%{buildroot}
%{__mv} %{buildroot}/usr/local/* %{buildroot}/usr/
%{__rm} -rf %{buildroot}/usr/local

%files
%defattr(-,root,root)
%{_bindir}/ruby-install
%{_datadir}/%{name}/*
%{_mandir}/man1/*
%doc
%{_defaultdocdir}/%{name}-%{version}/*

%{__mkdir_p} %{buildroot}%{_bindir}
%__ln_s /usr/local/bin/%{name} %{buildroot}%{_bindir}/%{name}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%defattr(-,root,root)
%{_bindir}/ruby-install
%{_datadir}/%{name}/*
%{_mandir}/man1/*
%doc
%{_defaultdocdir}/%{name}-*


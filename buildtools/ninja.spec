%define repo https://github.com/ninja-build/ninja
%define gitversion %(echo `curl -s https://github.com/ninja-build/ninja/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)

Name:           ninja
Version:        %{gitversion}
Release:        1.%{?dist}
Summary:        Ninja Build system
Group:          Development/Languages
License:        BSD
URL:            https://github.com/ninja-build/ninja

BuildRequires:	python >= 2.4, python-argparse, gcc, gcc-c++

%description
a small build system with a focus on speed http://ninja-build.org/

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update
git branch %{branch}

%build
cd %{name}-%{version}
echo Building..
./configure.py --bootstrap
./ninja manual

%install
cd %{name}-%{version}
%{__mkdir_p} %{buildroot}%{_bindir}
cp -p %{name} %{buildroot}%{_bindir}/%{name}


%clean
rm -rf %buildroot

%files
%defattr(0755, root, root)
%{_bindir}/%{name}

%include %{_rpmconfigdir}/macros.d/macros.rubygems
%global gem_name gem2rpm
%global remoteversion %(echo `gem list ^%{gem_name}$ -r |  grep %{gem_name} | cut -f2 -d" " | tr -d '()' | tr -d ','`)
%global rubyabi 2.2.4

Summary: Generate rpm specfiles from gems
Name: %{gem_name}
Version: %{remoteversion}
Release: 1.%{dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://rubyforge.org/projects/gem2rpm/
#Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: fedora.spec.erb
Source2: default.spec.erb  
Source3: fedora-17-18.spec.erb  
Source4: fedora-19-21.spec.erb  
Source5: fedora-21-rawhide.spec.erb
Source6: macros.rubygems
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems
BuildRequires: rubygems rubygems-devel
BuildRequires: ruby-devel
BuildArch: x86_64
Provides: rubygem-%{gem_name}
Provides: rubygem(%{gem_name})
%include %{SOURCE6}

%description
Generate source rpms and rpm spec files from a Ruby Gem.  The spec file tries
to follow the gem as closely as possible.

%prep

%setup -q -c -T
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{_builddir}/%{name}%{gem_dir} --bindir %{_builddir}/%{name}%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gem_name}

%build
%install
%__mkdir_p %{_builddir}/%{name}%{gem_dir}
%__mkdir_p %{_builddir}/%{name}%{_bindir}
find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;
cp -pa %{_builddir}/%{name}/* %{buildroot}/
find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \; 
cp -pa %{_builddir}/%{name}/* %{buildroot}/
cp -pR %{SOURCE1} %{buildroot}%{gemdir}/gems/%{name}-%{version}/templates/fedora.spec.erb
cp -pR %{SOURCE2} %{buildroot}%{gemdir}/gems/%{name}-%{version}/templates/default.spec.erb
cp -pR %{SOURCE3} %{buildroot}%{gemdir}/gems/%{name}-%{version}/templates/fedora-17-18.spec.erb
cp -pR %{SOURCE4} %{buildroot}%{gemdir}/gems/%{name}-%{version}/templates/fedora-19-21.spec.erb
cp -pR %{SOURCE5} %{buildroot}%{gemdir}/gems/%{name}-%{version}/templates/fedora-21-rawhide.spec.erb
if [ -f %{buildroot}%{gemdir}/bin ];then
  mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
  rm -rf %{buildroot}%{gemdir}/bin
fi
find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

if [ -f *.gemspec ]
then
    sed -e '/s.installed_by_version/ s/^#*/#/' -i  *.gemspec
fi
(
    cd %{buildroot}
    echo '%defattr(-,root,root,-)'
    if [ -d %{buildroot}%{gem_dir}/cache ]
    then
        echo '%exclude "%{gem_dir}/cache"'
    fi
    if [ -f %{buildroot}%{gem_dir}/cache/%{gem_name}-*.gem ]
    then
        echo '%exclude "%{gem_dir}/cache/%{gem_name}-*.gem"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gem_name}-*/.gitignore ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gem_name}-*/.gitignore"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gem_name}-*/.travis.yml ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gem_name}-*/.travis.yml"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gem_name}-*/.yardopts ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gem_name}-*/.yardopts"'
    fi
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache/%{gem_name}-*.gem'
) > filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/specifications"||' filelist
%{__sed} -i -e 's|%dir "%{_datadir}"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/build_info"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/doc"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/extensions"||' filelist
%{__sed} -i -e 's|%dir "%{gem_dir}/gems"||' filelist
%{__sed} -i -e 's|%dir "%{_exec_prefix}"||' filelist
%{__sed} -i -e 's|%dir "%{_bindir}"||' filelist
%{__sed} -i -e 's|%dir "%{_libdir}"||' filelist
%{__sed} -i -e 's|%dir "%{_libdir}/gems"||' filelist
%{__sed} -i -e 's|%dir "%{_libdir}/gems/ruby"||' filelist
%{__sed} -i -e 's/%dir ""//g' filelist
%{__sed} -i -e '/^$/d' filelist

if [ -f %{buildroot}%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec"
    sed -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
fi
if [ -f %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/%{gem_name}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/%{gem_name}.gemspec"
    sed -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/%{gem_name}.gemspec
fi

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f filelist


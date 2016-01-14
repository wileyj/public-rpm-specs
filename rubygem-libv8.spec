%if 0%{?el6}
    %define macro %{_rpmconfigdir}/macros.d/macros.python27
    %global __python /usr/bin/python27
%else
    %define macro %{_rpmconfigdir}/macros.d/macros.python
    %global __python /usr/bin/python
%endif
%include %{macro}

AutoReqProv: no
%include %{_rpmconfigdir}/macros.d/macros.rubygems
%global gemname libv8
%global remoteversion %(echo `gem list ^%{gemname}$ -r |  grep %{gemname} | cut -f2 -d" " | tr -d '()' | tr -d ','`)
%global rubyabi 2.2.2

Summary: Distribution of the V8 JavaScript engine
Name: rubygem-%{gemname}
Version: %{remoteversion}
Release: 1.%{dist}
Group: Development/Languages
License: Ruby
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems rubygem-mini_portile rubygem-nokogiri
BuildRequires: rubygems rubygems-devel
BuildRequires: ruby-devel
BuildRequires: ruby rubygems rubygem-mini_portile rubygem-nokogiri
BuildArch: x86_64
Provides: rubygem-%{gemname}
Provides: rubygem(%{gemname})

%description
Distributes the V8 JavaScript engine in binary and source forms in order to
support fast builds of The Ruby Racer.

%prep

%setup -q -c -T
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{_builddir}/%{name}%{gem_dir} --bindir %{_builddir}/%{name}%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gemname}

%build

%install
%__mkdir_p %{_builddir}/%{name}%{gem_dir}
%__mkdir_p %{_builddir}/%{name}%{_bindir}
/bin/sed -i -e 's|%{_bindir}/env python|%{python27}|g' %{_builddir}/%{name}/usr/share/gems/gems/libv8-4.5.95.5/vendor/v8/build/gyp_v8
/bin/sed -i -e 's|%{_bindir}/env python|%{python27}|g' %{_builddir}/%{name}/usr/share/gems/gems/libv8-4.5.95.5/vendor/depot_tools/external_bin/gsutil/gsutil_4.7/gsutil/third_party/boto/bin/route53
/bin/sed -i -e 's|%{_bindir}/env python|%{python27}|g' %{_builddir}/%{name}/usr/share/gems/gems/libv8-4.5.95.5/vendor/depot_tools/external_bin/gsutil/gsutil_4.7/gsutil/third_party/boto/bin/lss3

find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;
cp -pa %{_builddir}/%{name}/* %{buildroot}/
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
    if [ -f %{buildroot}%{gem_dir}/cache/%{gemname}-%{version}.gem ]
    then
        echo '%exclude "%{gem_dir}/cache/%{gemname}-%{version}.gem"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/.gitignore ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-%{version}/.gitignore"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/.travis.yml ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-%{version}/.travis.yml"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/.yardopts ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-%{version}/.yardopts"'
    fi
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache/%{gemname}-%{version}.gem'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/build/gyp"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/build/gyp_v8"'
    #echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/gyp/*"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/tools/*"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/test/*"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/PRESUBMIT.pyc"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/PRESUBMIT.pyo"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/third_party"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/testing/gtest"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/testing/gmock"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/testing"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/buildtools/clang_format"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/buildtools/checkdeps"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8/build"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/v8"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/depot_tools"'
    echo '"%{gem_dir}/gems/%{gemname}-%{version}/vendor/depot_tools/external_bin"'
) > filelist
%{__sed} -i -e 's|%dir ""||g' filelist

if [ -f %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec"
    sed -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/specifications/%{gemname}-%{version}.gemspec
fi
if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec ]
then
    echo "Making changes using sed to %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec"
    sed -i -e 's|\["= |\[">= |g' %{buildroot}%{gem_dir}/gems/%{gemname}-%{version}/%{gemname}.gemspec
fi





%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f filelist


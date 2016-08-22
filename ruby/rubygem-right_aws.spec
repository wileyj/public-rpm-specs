#AutoReqProv: no
#  gem list ^json$ -r |  cut -f2 -d" " | grep -o '\((.*\)$' | tr -d '()'
%include %{_rpmconfigdir}/macros.d/macros.rubygems
%global gemname right_aws
%global remoteversion %(echo `gem list ^%{gemname}$ -r |  grep %{gemname} | cut -f2 -d" " | tr -d '()' | tr -d ','`)
%global rubyabi 2.2.2
%define filelist %{name}-%{version}-filelist

Summary: The RightScale AWS gems have been designed to provide a robust, fast, and secure interface to Amazon EC2, EBS, S3, SQS, SDB, and CloudFront
Name: rubygem-%{gemname}
Version: %{remoteversion}
Release: 1.%{dist}
Group: Development/Languages
License: Ruby
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems
Requires: rubygem-right_http_connection
BuildRequires: rubygems rubygems-devel
BuildRequires: ruby ruby-devel
BuildArch: x86_64
Provides: rubygem-%{gemname}
Provides: rubygem(%{gemname})

%description
== DESCRIPTION:
The RightScale AWS gems have been designed to provide a robust, fast, and
secure interface to Amazon EC2, EBS, S3, SQS, SDB, and CloudFront.
These gems have been used in production by RightScale since late 2006 and are
being maintained to track enhancements made by Amazon.
The RightScale AWS gems comprise:
- RightAws::Ec2 -- interface to Amazon EC2 (Elastic Compute Cloud) and the
associated EBS (Elastic Block Store)
- RightAws::S3 and RightAws::S3Interface -- interface to Amazon S3 (Simple
Storage Service)
- RightAws::Sqs and RightAws::SqsInterface -- interface to first-generation
Amazon SQS (Simple Queue Service) (API version 2007-05-01)
- RightAws::SqsGen2 and RightAws::SqsGen2Interface -- interface to
second-generation Amazon SQS (Simple Queue Service) (API version 2008-01-01)
- RightAws::SdbInterface and RightAws::ActiveSdb -- interface to Amazon SDB
(SimpleDB)
- RightAws::AcfInterface -- interface to Amazon CloudFront, a content
distribution service
== FEATURES:
- Full programmmatic access to EC2, EBS, S3, SQS, SDB, and CloudFront.
- Complete error handling: all operations check for errors and report complete
error information by raising an AwsError.
- Persistent HTTP connections with robust network-level retry layer using
RightHttpConnection).  This includes socket timeouts and retries.
- Robust HTTP-level retry layer.  Certain (user-adjustable) HTTP errors
returned
by Amazon's services are classified as temporary errors.
These errors are automaticallly retried using exponentially increasing
intervals.
The number of retries is user-configurable.
- Fast REXML-based parsing of responses (as fast as a pure Ruby solution
allows).
- Uses libxml (if available) for faster response parsing.
- Support for large S3 list operations.  Buckets and key subfolders containing
many (> 1000) keys are listed in entirety.  Operations based on list (like
bucket clear) work on arbitrary numbers of keys.
- Support for streaming GETs from S3, and streaming PUTs to S3 if the data
source is a file.
- Support for single-threaded usage, multithreaded usage, as well as usage
with multiple
AWS accounts.
- Support for both first- and second-generation SQS (API versions 2007-05-01
and 2008-01-01).  These versions of SQS are not compatible.
- Support for signature versions 0 and 1 on SQS, SDB, and EC2.
- Interoperability with any cloud running Eucalyptus
(http://eucalyptus.cs.ucsb.edu)
- Test suite (requires AWS account to do "live" testing).

%prep


export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{_builddir}/%{name}%{gem_dir} --bindir %{_builddir}/%{name}%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gemname}

%build

%install
%__mkdir_p %{_builddir}/%{name}%{gem_dir}
%__mkdir_p %{_builddir}/%{name}%{_bindir}
find %{_builddir}/%{name} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;
cp -pa %{_builddir}/%{name}/* %{buildroot}/
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
    if [ -f %{buildroot}%{gem_dir}/cache/%{gemname}-*.gem ]
    then
        echo '%exclude "%{gem_dir}/cache/%{gemname}-*.gem"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-*/.gitignore ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-*/.gitignore"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-*/.travis.yml ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-*/.travis.yml"'
    fi
    if [ -f %{buildroot}%{gem_dir}/gems/%{gemname}-*/.yardopts ]
    then
        echo '%exclude "%{gem_dir}/gems/%{gemname}-*/.yardopts"'
    fi
    find %{buildroot} -type d -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache'
    find %{buildroot} -type f -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g' | %{__grep} -v '%{gem_dir}/cache/%{gemname}-*.gem'
) >  %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/specifications"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_datadir}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/build_info"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/doc"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/extensions"||' %{filelist}
%{__sed} -i -e 's|%dir "%{gem_dir}/gems"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_exec_prefix}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_bindir}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_libdir}"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_libdir}/gems"||' %{filelist}
%{__sed} -i -e 's|%dir "%{_libdir}/gems/ruby"||' %{filelist}
%{__sed} -i -e 's/%dir ""//g' %{filelist}
%{__sed} -i -e '/^$/d' %{filelist}

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
%__rm -rf %{filelist}
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f  %{filelist}


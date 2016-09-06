%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

%define repo https://github.com/vim/vim.git

%define patchlevel 909
%define WITH_SELINUX 0
%define desktop_file 0
%define withnetbeans 0
%define withvimspell 0
%define withhunspell 0
%define withruby 1
%define baseversion 7.4
%define vimdir vim74
%define realname vim

Summary: The VIM editor
Name: git-vim
Version: %{baseversion}.%{patchlevel}
Release: 3.%{?dist}
License: Vim
Group: Applications/Editors
URL: https://github.com/%{realname}/%{realname}.git
Source1: vimrc

Buildroot: %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ncurses-devel gettext perl-devel
BuildRequires: perl-ExtUtils-Embed perl-ExtUtils-ParseXS
BuildRequires: libacl-devel gpm-devel autoconf
Buildrequires: ruby-devel ruby
Epoch: 2
Conflicts: filesystem < 3

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package common
Summary: The common files needed by any version of the VIM editor
Group: Applications/Editors
Conflicts: man-pages-fr < 0.9.7-14
Conflicts: man-pages-it < 0.3.0-17
Conflicts: man-pages-pl < 0.24-2
Requires: %{realname}-filesystem

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.

%package spell
Summary: The dictionaries for spell checking. This package is optional
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release}

%description spell
This subpackage contains dictionaries for vim spell checking in
many different languages.

%package minimal
Summary: A minimal version of the VIM editor
Group: Applications/Editors
Provides: vi = %{version}-%{release}
Provides: /bin/vi

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present. NOTE: The online help is only available when the vim-common
package is installed.

%package enhanced
Summary: A version of the VIM editor which includes recent enhancements
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} which
Provides: vim = %{version}-%{release}
Requires: perl

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.

%package filesystem
Summary: VIM filesystem layout
Group: Applications/Editors

%description filesystem
This package provides some directories which are required by other
packages that add vim files, p.e.  additional syntax files or filetypes.

#%setup -q -b 0 -n %{vimdir}
#git clone https://github.com/vim/vim.git


%prep
if [ -d %{realname}-%{version} ];then
    rm -rf %{realname}-%{version}
fi
git clone %{repo} %{realname}-%{version}
cd %{realname}-%{version}
git submodule init
git submodule update

chmod -x runtime/tools/mve.awk
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

%build
cd %{realname}-%{version}/src
autoconf

sed -e "s+VIMRCLOC  = \$(VIMLOC)+VIMRCLOC   = /etc+" Makefile > Makefile.tmp
mv -f Makefile.tmp Makefile

export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"

%configure --prefix=%{_prefix} --with-features=huge \
 --enable-pythoninterp=dynamic \
 --enable-perlinterp \
 --disable-tclinterp \
 --with-x=no \
 --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
 --enable-cscope --with-modified-by="<bugzilla@redhat.com>" \
 --with-tlib=tinfo \
 --with-compiledby="<bugzilla@redhat.com>" \
  --disable-netbeans \
  --disable-selinux \
  --enable-rubyinterp=dynamic \


make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim enhanced-vim
make clean

%install
cd %{realname}-%{version}
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/%{realname}/vimfiles/{after,autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
mkdir -p %{buildroot}/%{_datadir}/%{realname}/vimfiles/after/{autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
cp runtime/doc/uganda.txt LICENSE
rm -f README*.info


cd src
make install DESTDIR=%{buildroot} BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
make installgtutorbin  DESTDIR=%{buildroot} BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m755 vim %{buildroot}%{_bindir}/vi
install -m755 enhanced-vim %{buildroot}%{_bindir}/vim

(   
    cd %{buildroot}
    ln -sf vi ./%{_bindir}/rvi
    ln -sf vi ./%{_bindir}/rview
    ln -sf vi ./%{_bindir}/view
    ln -sf vi ./%{_bindir}/ex
    ln -sf vim ./%{_bindir}/rvim
    ln -sf vim ./%{_bindir}/vimdiff
    perl -pi -e "s,%{buildroot},," .%{_mandir}/man1/vim.1 .%{_mandir}/man1/vimtutor.1
    rm -f .%{_mandir}/man1/rvim.1
    ln -sf vim.1.gz .%{_mandir}/man1/vi.1.gz
    ln -sf vim.1.gz .%{_mandir}/man1/rvi.1.gz
    ln -sf vim.1.gz .%{_mandir}/man1/vimdiff.1.gz
    ( 
        cd ./%{_datadir}/%{realname}/%{vimdir}/lang; ln -sf menu_ja_jp.ujis.vim menu_ja_jp.eucjp.vim 
    )
)

pushd %{buildroot}/%{_datadir}/%{realname}/%{vimdir}/tutor
mkdir conv
   iconv -f CP1252 -t UTF8 tutor.ca > conv/tutor.ca
   iconv -f CP1252 -t UTF8 tutor.it > conv/tutor.it
   iconv -f CP1252 -t UTF8 tutor.fr > conv/tutor.fr
   iconv -f CP1252 -t UTF8 tutor.es > conv/tutor.es
   iconv -f CP1252 -t UTF8 tutor.de > conv/tutor.de
   iconv -f UTF8 -t UTF8 tutor.ja.utf-8 > conv/tutor.ja.utf-8
   iconv -f UTF8 -t UTF8 tutor.ko.utf-8 > conv/tutor.ko.utf-8
   iconv -f CP1252 -t UTF8 tutor.no > conv/tutor.no
   iconv -f ISO-8859-2 -t UTF8 tutor.pl > conv/tutor.pl
   iconv -f ISO-8859-2 -t UTF8 tutor.sk > conv/tutor.sk
   iconv -f KOI8R -t UTF8 tutor.ru > conv/tutor.ru
   iconv -f CP1252 -t UTF8 tutor.sv > conv/tutor.sv
   mv -f tutor.ja.euc tutor.ja.sjis tutor.ko.euc tutor.pl.cp1250 tutor.zh.big5 tutor.ru.cp1251 tutor.zh.euc conv/
   rm -f tutor.ca tutor.de tutor.es tutor.fr tutor.gr tutor.it tutor.ja.utf-8 tutor.ko.utf-8 tutor.no tutor.pl tutor.sk tutor.ru tutor.sv
mv -f conv/* .
rmdir conv
popd

chmod 644 %{buildroot}/%{_datadir}/%{realname}/%{vimdir}/doc/vim2html.pl %{buildroot}/%{_datadir}/%{realname}/%{vimdir}/tools/*.pl %{buildroot}/%{_datadir}/%{realname}/%{vimdir}/tools/vim132
chmod 644 ../runtime/doc/vim2html.pl

mkdir -p %{buildroot}/%{_sysconfdir}/profile.d
cat >%{buildroot}/%{_sysconfdir}/profile.d/vim.sh <<EOF
if [ -n "\$BASH_VERSION" -o -n "\$KSH_VERSION" -o -n "\$ZSH_VERSION" ]; then
    [ -x %{_bindir}/id ] || return
    ID=\`/usr/bin/id -u\`
    [ -n "\$ID" -a "\$ID" -le 200 ] && return
    alias vi >/dev/null 2>&1 || alias vi=vim
fi
EOF
cat >%{buildroot}/%{_sysconfdir}/profile.d/vim.csh <<EOF
if ( -x /usr/bin/id ) then
    if ( "\`/usr/bin/id -u\`" > 200 ) then
        alias vi vim
    endif
endif
EOF
mkdir -p %{buildroot}/%{_sysconfdir}/profile.d
install -p -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/vimrc
install -p -m644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/virc

(
    cd %{buildroot}/%{_datadir}/%{realname}/%{vimdir}/doc;
    gzip -9 *.txt
    gzip -d help.txt.gz version7.txt.gz sponsor.txt.gz
    cat tags | sed -e 's/\t\(.*.txt\)\t/\t\1.gz\t/;s/\thelp.txt.gz\t/\thelp.txt\t/;s/\tversion7.txt.gz\t/\tversion7.txt\t/;s/\tsponsor.txt.gz\t/\tsponsor.txt\t/' > tags.new; mv -f tags.new tags
cat >> tags << EOF
vi_help.txt vi_help.txt /*vi_help.txt*
vi-author.txt   vi_help.txt /*vi-author*
vi-Bram.txt vi_help.txt /*vi-Bram*
vi-Moolenaar.txt    vi_help.txt /*vi-Moolenaar*
vi-credits.txt  vi_help.txt /*vi-credits*
EOF
LANG=C sort tags > tags.tmp; mv tags.tmp tags
 )

( cd ../runtime; rm -rf doc; ln -svf ../../vim/%{vimdir}/doc docs; ) 
rm -f %{buildroot}/%{_datadir}/vim/%{vimdir}/macros/maze/maze*.c
rm -rf %{buildroot}/%{_datadir}/vim/%{vimdir}/tools
rm -rf %{buildroot}/%{_datadir}/vim/%{vimdir}/doc/vim2html.pl
rm -f %{buildroot}/%{_datadir}/vim/%{vimdir}/tutor/tutor.gr.utf-8~
( 
    cd %{buildroot}/%{_mandir}
    for i in `find ??/ -type f`; do
        bi=`basename $i`
        iconv -f latin1 -t UTF8 $i > %{buildroot}/$bi
        mv -f %{buildroot}/$bi $i
    done
)

# Remove not UTF-8 manpages
for i in pl.ISO8859-2 it.ISO8859-1 ru.KOI8-R fr.ISO8859-1; do
    rm -rf %{buildroot}/%{_mandir}/$i
done

# use common man1/ru directory
mv %{buildroot}/%{_mandir}/ru.UTF-8 %{buildroot}/%{_mandir}/ru

# Remove duplicate man pages
for i in fr.UTF-8 it.UTF-8 pl.UTF-8; do
    rm -rf %{buildroot}/%{_mandir}/$i
done
echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man1/rvim.1

mkdir -p %{buildroot}/%{_mandir}/man5
echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man5/virc.5
echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man5/vimrc.5
touch %{buildroot}/%{_datadir}/%{realname}/vimfiles/doc/tags

# delete files we don't want
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/check_locales.vim
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/cleanadd.vim
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/en.ascii.spl
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/en.ascii.sug
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/en.latin1.spl
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/en.latin1.sug
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/en.utf-8.spl
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/en.utf-8.sug
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/fixdup.vim
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/he.vim
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/spell.vim
rm -rf %{buildroot}%{_datadir}/%{realname}/%{vimdir}/spell/yi.vim;
rm -rf %{buildroot}%{_bindir}/gvimtutor
rm -rf %{buildroot}%{_mandir}/man1/evim*
rm -rf %{buildroot}%{_mandir}/man1/eview*
rm -rf %{buildroot}%{_mandir}/man1/gview*
rm -rf %{buildroot}%{_mandir}/man1/gvim*
rm -rf %{buildroot}%{_mandir}/man1/gvimdiff*
rm -rf %{buildroot}%{_mandir}/man1/rgview*
rm -rf %{buildroot}%{_mandir}/man1/rgvim*
rm -rf %{buildroot}%{_bindir}/eview*
rm -rf %{buildroot}%{_bindir}/evim*
rm -rf %{buildroot}%{_bindir}/gview*
rm -rf %{buildroot}%{_bindir}/gvim*
rm -rf %{buildroot}%{_bindir}/rgview*
rm -rf %{buildroot}%{_bindir}/rgvim*
rm -rf %{buildroot}%{_datadir}/applications
rm -rf %{buildroot}%{_datadir}/icons

for i in `ls %{buildroot}%{_mandir}/man1`; do
    mv %{buildroot}%{_mandir}/man1/$i %{buildroot}%{_mandir}/man1/%{realname}-$i
done
for i in `ls %{buildroot}%{_mandir}/man5`; do
    mv %{buildroot}%{_mandir}/man5/$i %{buildroot}%{_mandir}/man5/%{realname}-$i
done

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{realname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{realname}-%{version}
[ "%{_builddir}/%{realname}" != "/" ] && %__rm -rf %{_builddir}/%{realname}

%files common
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/vimrc
#%doc runtime/docs
%dir %{_datadir}/%{realname}
%dir %{_datadir}/%{realname}/%{vimdir}
%{_datadir}/%{realname}/%{vimdir}/autoload
%{_datadir}/%{realname}/%{vimdir}/colors
%{_datadir}/%{realname}/%{vimdir}/compiler
%{_datadir}/%{realname}/%{vimdir}/doc
%{_datadir}/%{realname}/%{vimdir}/*.vim
%{_datadir}/%{realname}/%{vimdir}/ftplugin
%{_datadir}/%{realname}/%{vimdir}/indent
%{_datadir}/%{realname}/%{vimdir}/keymap
%{_datadir}/%{realname}/%{vimdir}/lang/*.vim
%{_datadir}/%{realname}/%{vimdir}/lang/*.txt
%dir %{_datadir}/%{realname}/%{vimdir}/lang
%{_datadir}/%{realname}/%{vimdir}/macros
%{_datadir}/%{realname}/%{vimdir}/plugin
%{_datadir}/%{realname}/%{vimdir}/print
%{_datadir}/%{realname}/%{vimdir}/syntax
%{_datadir}/%{realname}/%{vimdir}/tutor
%{_datadir}/%{realname}/vim74/pack/dist/opt/matchit/doc/matchit.txt
%{_datadir}/%{realname}/vim74/pack/dist/opt/matchit/doc/tags
%{_datadir}/%{realname}/vim74/pack/dist/opt/matchit/plugin/matchit.vim

/%{_bindir}/xxd
%{_mandir}/man1/%{realname}-ex.*
%{_mandir}/man1/%{realname}-rvi.*
%{_mandir}/man1/%{realname}-rview.*
%{_mandir}/man1/%{realname}-vi.*
%{_mandir}/man1/%{realname}-view.*
%{_mandir}/man1/%{realname}-rvim.*
%{_mandir}/man1/%{realname}-vim.*
%{_mandir}/man1/%{realname}-vimdiff.*
%{_mandir}/man1/%{realname}-vimtutor.*
%{_mandir}/man1/%{realname}-xxd.*
%{_mandir}/man5/%{realname}-vimrc.*
%lang(fr) %{_mandir}/fr/man1/*
%lang(it) %{_mandir}/it/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%lang(ru) %{_mandir}/ru/man1/*
%lang(af) %{_datadir}/%{realname}/%{vimdir}/lang/af
%lang(ca) %{_datadir}/%{realname}/%{vimdir}/lang/ca
%lang(cs) %{_datadir}/%{realname}/%{vimdir}/lang/cs
%lang(cs.cp1250) %{_datadir}/%{realname}/%{vimdir}/lang/cs.cp1250
%lang(de) %{_datadir}/%{realname}/%{vimdir}/lang/de
%lang(en_GB) %{_datadir}/%{realname}/%{vimdir}/lang/en_GB
%lang(eo) %{_datadir}/%{realname}/%{vimdir}/lang/eo
%lang(es) %{_datadir}/%{realname}/%{vimdir}/lang/es
%lang(fi) %{_datadir}/%{realname}/%{vimdir}/lang/fi
%lang(fr) %{_datadir}/%{realname}/%{vimdir}/lang/fr
%lang(ga) %{_datadir}/%{realname}/%{vimdir}/lang/ga
%lang(it) %{_datadir}/%{realname}/%{vimdir}/lang/it
%lang(ja) %{_datadir}/%{realname}/%{vimdir}/lang/ja
%lang(ja.euc-jp) %{_datadir}/%{realname}/%{vimdir}/lang/ja.euc-jp
%lang(ja.sjis) %{_datadir}/%{realname}/%{vimdir}/lang/ja.sjis
%lang(ko) %{_datadir}/%{realname}/%{vimdir}/lang/ko
%lang(ko) %{_datadir}/%{realname}/%{vimdir}/lang/ko.UTF-8
%lang(nb) %{_datadir}/%{realname}/%{vimdir}/lang/nb
%lang(nl) %{_datadir}/%{realname}/%{vimdir}/lang/nl
%lang(no) %{_datadir}/%{realname}/%{vimdir}/lang/no
%lang(pl) %{_datadir}/%{realname}/%{vimdir}/lang/pl
%lang(pl.UTF-8) %{_datadir}/%{realname}/%{vimdir}/lang/pl.UTF-8
%lang(pl.cp1250) %{_datadir}/%{realname}/%{vimdir}/lang/pl.cp1250
%lang(pt_BR) %{_datadir}/%{realname}/%{vimdir}/lang/pt_BR
%lang(ru) %{_datadir}/%{realname}/%{vimdir}/lang/ru
%lang(ru.cp1251) %{_datadir}/%{realname}/%{vimdir}/lang/ru.cp1251
%lang(sk) %{_datadir}/%{realname}/%{vimdir}/lang/sk
%lang(sk.cp1250) %{_datadir}/%{realname}/%{vimdir}/lang/sk.cp1250
%lang(sv) %{_datadir}/%{realname}/%{vimdir}/lang/sv
%lang(uk) %{_datadir}/%{realname}/%{vimdir}/lang/uk
%lang(uk.cp1251) %{_datadir}/%{realname}/%{vimdir}/lang/uk.cp1251
%lang(vi) %{_datadir}/%{realname}/%{vimdir}/lang/vi
%lang(zh_CN) %{_datadir}/%{realname}/%{vimdir}/lang/zh_CN
%lang(zh_CN.cp936) %{_datadir}/%{realname}/%{vimdir}/lang/zh_CN.cp936
%lang(zh_TW) %{_datadir}/%{realname}/%{vimdir}/lang/zh_TW
%lang(zh_CN.UTF-8) %{_datadir}/%{realname}/%{vimdir}/lang/zh_CN.UTF-8
%lang(zh_TW.UTF-8) %{_datadir}/%{realname}/%{vimdir}/lang/zh_TW.UTF-8

%files minimal
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/virc
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvi
%{_bindir}/rview
%{_mandir}/man1/%{realname}-vim.*
%{_mandir}/man1/%{realname}-vi.*
%{_mandir}/man1/%{realname}-ex.*
%{_mandir}/man1/%{realname}-rvi.*
%{_mandir}/man1/%{realname}-rview.*
%{_mandir}/man1/%{realname}-view.*
%{_mandir}/man5/%{realname}-virc.*

%files enhanced
%defattr(-,root,root)
%{_bindir}/vim
%{_bindir}/rvim
%{_bindir}/vimdiff
%{_bindir}/vimtutor
%config(noreplace) %{_sysconfdir}/profile.d/vim.*
%{_datadir}/%{realname}/%{realname}74/pack/dist/opt/dvorak/dvorak/disable.vim
%{_datadir}/%{realname}/%{realname}74/pack/dist/opt/dvorak/dvorak/enable.vim
%{_datadir}/%{realname}/%{realname}74/pack/dist/opt/dvorak/plugin/dvorak.vim
%{_datadir}/%{realname}/%{realname}74/pack/dist/opt/editexisting/plugin/editexisting.vim
%{_datadir}/%{realname}/%{realname}74/pack/dist/opt/justify/plugin/justify.vim
%{_datadir}/%{realname}/%{realname}74/pack/dist/opt/shellmenu/plugin/shellmenu.vim
%{_datadir}/%{realname}/%{realname}74/pack/dist/opt/swapmouse/plugin/swapmouse.vim
%{_datadir}/%{realname}/%{realname}74/rgb.txt

%files filesystem
%defattr(-,root,root)
%dir %{_datadir}/%{realname}/vimfiles
%dir %{_datadir}/%{realname}/vimfiles/after
%dir %{_datadir}/%{realname}/vimfiles/after/*
%dir %{_datadir}/%{realname}/vimfiles/autoload
%dir %{_datadir}/%{realname}/vimfiles/colors
%dir %{_datadir}/%{realname}/vimfiles/compiler
%dir %{_datadir}/%{realname}/vimfiles/doc
%ghost %{_datadir}/%{realname}/vimfiles/doc/tags
%dir %{_datadir}/%{realname}/vimfiles/ftdetect
%dir %{_datadir}/%{realname}/vimfiles/ftplugin
%dir %{_datadir}/%{realname}/vimfiles/indent
%dir %{_datadir}/%{realname}/vimfiles/keymap
%dir %{_datadir}/%{realname}/vimfiles/lang
%dir %{_datadir}/%{realname}/vimfiles/plugin
%dir %{_datadir}/%{realname}/vimfiles/print
%dir %{_datadir}/%{realname}/vimfiles/spell
%dir %{_datadir}/%{realname}/vimfiles/syntax
%dir %{_datadir}/%{realname}/vimfiles/tutor


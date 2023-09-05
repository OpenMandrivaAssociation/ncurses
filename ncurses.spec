%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define date 20230902
%define major 6
%define majorminor 6.4
%define utf8libname %mklibname %{name}w
%define oldutf8libname %mklibname %{name}w %{major}
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}
%define utf8devname %mklibname -d %{name}w
%define staticname %mklibname -d -s %{name}
%global optflags %{optflags} -Oz
%global build_ldflags %{build_ldflags} -ldl

%bcond_without cplusplus
%bcond_with gpm

# ugly as fuck, but at least mostly harmless to children and animals..
%define libgen()\
%package -n %2%{_lib}%{1}\
Summary:	Ncurses %{1} library\
Group:		System/Libraries\
Conflicts:	%{_lib}ncurses%{major} < 5.9-6.20120922.1 \
Conflicts:	%{_lib}ncursesw%{major} < 5.9-6.20120922.1 \
Obsoletes:	%2%{_lib}%{1}%{4} < %{EVRD} \
Provides:	%2%{_lib}%{1}%{4} = %{EVRD} \
\
%description -n %2%{_lib}%{1}%{4}\
This package comes with lib%{1} from the ncurses library.\
\
%files -n %2%{_lib}%{1}%{4}\
%{3}%{_libdir}/lib%{1}.so.%{4}*\
%{nil}

Summary:	A CRT screen handling and optimization package
Name:		ncurses
Version:	6.4
%if "%{date}" != ""
Release:	0.%{date}.1
Source0:	https://invisible-mirror.net/archives/ncurses/current/%{name}-%{version}-%{date}.tgz
%else
Release:	1
Source0:	ftp://ftp.invisible-island.net/ncurses/%{name}-%{version}.tar.gz
%endif
License:	MIT
Group:		System/Libraries
Url:		http://www.gnu.org/software/ncurses/ncurses.html
Source4:	ncurses-resetall.sh
Source5:	ncurses-useful-terms
Source6:	ncurses.rpmlintrc
Patch1:		ncurses-5.6-xterm-debian.patch
# regenerating configure needs patched autoconf, so modify configure
# directly
Patch2:		ncurses-6.4-fix-ld-searchpath-detection.patch
Patch3:		ncurses-5.9-buildfix.patch
Patch4:		ncurses-6.4-no-Lusrlib.patch
Patch7:		ncurses-urxvt.patch
%if %{with gpm}
BuildRequires:	gpm-devel
%endif
BuildRequires:	sharutils
Conflicts:	%{name}-extraterms < 5.9-6.20121026.3
%if %{with compat32}
BuildRequires:	libc6
%endif

%description
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

# to be killed
###############################################################################
%package -n %{libname}
Summary:	The development files for applications which use ncurses
Group:		System/Libraries
%if "%_lib" == "lib64"
Provides:	libtinfo.so.6()(64bit)
%else
Provides:	libtinfo.so.6
%endif

%description -n %{libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.


%libpackage form %{major}
%libpackage menu %{major}
%libpackage panel %{major}

%libpackage formw %{major}
%libpackage menuw %{major}
%libpackage panelw %{major}

%if %{with cplusplus}
%libpackage ncurses++ %{major}
%libpackage ncurses++w %{major}
%endif

%package -n %{utf8libname}
Summary:	Ncurses libraries which support UTF8
Group:		System/Libraries
%rename %{oldutf8libname}

%description -n %{utf8libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

This package contains ncurses libraries which support wide char (UTF8),
and is not compatible with those without.

%package extraterms
Summary:	Some exotic terminal descriptions
Group:		System/Libraries
BuildArch:	noarch

%description extraterms
Install the ncurses-extraterms package if you use some exotic terminals.

%package -n %{devname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
# just keep this depdenency for untangling initial dependency issues..
%if "%{_lib}" == "lib64"
Provides:	devel(libncurses(64bit))
%else
Provides:	devel(libncurses)
%endif
Provides:	ncursesw-devel = %{version}-%{release}
Requires:	%{utf8libname} = %{version}
Requires:	%{_lib}formw = %{version}
Requires:	%{_lib}menuw = %{version}
Requires:	%{_lib}panelw = %{version}
# /usr/include/termcap.h conflicts
Conflicts:	termcap-devel > 2.0.8-53
Conflicts:	ncurses < 5.9-7.20131123.1

Obsoletes:	%mklibname -d %name 5
Obsoletes:	%mklibname -d %{name}w 5
Conflicts:	%{_lib}ncurses-devel < 5.7-3.20091128.2
%rename		%{utf8devname}

%description -n %{devname}
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package -n %{staticname}
Summary:	Static libraries for applications which use ncurses
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
Static libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses and link them statically.

%package -n termcap
Summary:	The terminal feature database used by certain applications
Group:		System/Libraries
BuildArch:	noarch

%description -n termcap
The termcap package provides the /etc/termcap file.  /etc/termcap is
a database which defines the capabilities of various terminals and
terminal emulators.  Certain programs use the /etc/termcap file to
access various features of terminals (the bell, colors, and graphics,
etc.).

%prep
%autosetup -p1 -n %{name}-%{version}%{?date:-%{date}}

find . -name "*.orig" -o -name "*~" | xargs rm -f
# fix some permissions
chmod 755 c++/edit_cfg.sh test/listused.sh test/configure test/tracemunch

# we don't need nor want this, and it also pulls in a dependency on /usr/bin/make
rm -rf test/package

# FIXME workaround for misdetection when using musl
sed -i -e 's,#if HAVE_GETTTYNAM,#if 0,g' progs/tset.c

# Pull in support for newer architectures and OSes
cp -f %{_datadir}/libtool/config/config.{guess,sub} .

%build
export PKG_CONFIG_LIBDIR=%{_libdir}/pkgconfig

CONFIGURE_TOP="$PWD"

%if %{with compat32}
mkdir -p ncurses-normal-32
cd ncurses-normal-32
export CC=gcc
export CXX=g++
export CFLAGS="$(echo %{optflags} |sed -e 's, -m64,,g') -m32"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="$CFLAGS"
export AR=llvm-ar
export RANLIB=llvm-ranlib
../configure \
	--prefix=%{_prefix} \
	--libdir=%{_prefix}/lib \
	--with-pkg-config-libdir=%{_prefix}/lib/pkgconfig \
	--without-libtool \
	--with-shared \
	--with-normal \
%if %{with cplusplus}
	--with-cxx \
	--with-cxx-shared \
%else
	--without-cxx \
%endif
	--without-debug \
	--enable-overwrite \
	--without-profile \
%if %{with gpm}
	--with-gpm --with-dlsym \
%endif
	--enable-termcap \
	--enable-getcap \
	--enable-const \
	--enable-hard-tabs \
	--enable-hash-map \
	--enable-no-padding \
	--enable-sigwinch \
	--enable-pc-files \
	--without-ada \
	--disable-widec \
	--enable-xmc-glitch \
	--enable-colorfgbg \
	--with-ospeed=unsigned \
	--disable-wattr-macros \
	--without-progs \
	--disable-stripping

%make_build
cd ..

mkdir -p ncurses-utf8-32
cd ncurses-utf8-32
%configure \
	--prefix=%{_prefix} \
	--libdir=%{_prefix}/lib \
	--with-pkg-config-libdir=%{_prefix}/lib/pkgconfig \
	--without-libtool \
	--with-shared \
	--with-normal \
%if %{with cplusplus}
	--with-cxx \
	--with-cxx-shared \
%else
	--without-cxx \
%endif
	--without-debug \
	--enable-overwrite \
	--without-profile \
%if %{with gpm}
	--with-gpm --with-dlsym \
%endif
	--enable-termcap \
	--enable-getcap \
	--enable-const \
	--enable-hard-tabs \
	--enable-hash-map \
	--enable-no-padding \
	--enable-sigwinch \
	--without-ada \
	--enable-widec \
	--enable-xmc-glitch \
	--enable-colorfgbg \
	--enable-pc-files \
	--enable-ext-colors \
	--enable-ext-mouse \
	--with-ospeed=unsigned \
	--disable-wattr-macros \
	--enable-sp-funcs \
	--disable-stripping

%make_build
cd -
unset CFLAGS
unset CXXFLAGS
unset LDFLAGS
unset AR
unset RANLIB
unset CC
unset CXX
%endif

mkdir -p ncurses-normal
cd ncurses-normal
%configure \
	--without-libtool \
	--with-pkg-config-libdir=%{_libdir}/pkgconfig \
	--with-shared \
	--with-normal \
%if %{with cplusplus}
	--with-cxx \
	--with-cxx-shared \
%else
	--without-cxx \
%endif
	--without-debug \
	--enable-overwrite \
	--without-profile \
%if %{with gpm}
	--with-gpm --with-dlsym \
%endif
	--enable-termcap \
	--enable-getcap \
	--enable-const \
	--enable-hard-tabs \
	--enable-hash-map \
	--enable-no-padding \
	--enable-sigwinch \
	--without-ada \
	--disable-widec \
	--enable-xmc-glitch \
	--enable-colorfgbg \
	--disable-pc-files \
	--with-ospeed=unsigned \
	--disable-wattr-macros \
	--without-progs \
	--disable-stripping

%make_build
cd -

mkdir -p ncurses-utf8
cd ncurses-utf8
%configure \
	--without-libtool \
	--with-pkg-config-libdir=%{_libdir}/pkgconfig \
	--with-shared \
	--with-normal \
%if %{with cplusplus}
	--with-cxx \
	--with-cxx-shared \
%else
	--without-cxx \
%endif
	--without-debug \
	--enable-overwrite \
	--without-profile \
%if %{with gpm}
	--with-gpm --with-dlsym \
%endif
	--enable-termcap \
	--enable-getcap \
	--enable-const \
	--enable-hard-tabs \
	--enable-hash-map \
	--enable-no-padding \
	--enable-sigwinch \
	--without-ada \
	--enable-widec \
	--enable-xmc-glitch \
	--enable-colorfgbg \
	--enable-pc-files \
	--enable-ext-colors \
	--enable-ext-mouse \
	--with-ospeed=unsigned \
	--disable-wattr-macros \
	--enable-sp-funcs \
	--disable-stripping
	
%make_build
cd -

%install
%if %{with compat32}
cd ncurses-normal-32
%make_install

cd ../ncurses-utf8-32
%make_install

cd ..
%endif

cd ncurses-normal
%make_install
cd -

cd ncurses-utf8
%make_install
cd -

# the resetall script
install -m 755 %{SOURCE4} %{buildroot}%{_bindir}/resetall

# we don't want this in doc
rm -f c++/demo

for i in form menu ncurses panel; do
    ln -sf lib${i}w.a %{buildroot}%{_libdir}/lib${i}.a
    ln -sf lib${i}w.so %{buildroot}%{_libdir}/lib${i}.so
done

%if %{with cplusplus}
ln -sf libncurses++w.so %{buildroot}%{_libdir}/libncurses++.so
ln -sf libncurses++w.a %{buildroot}%{_libdir}/libncurses++.a
%endif

#
# FIXME
# OK do not time to debug it now
#
cp %{buildroot}%{_datadir}/terminfo/x/xterm %{buildroot}%{_datadir}/terminfo/x/xterm2
cp %{buildroot}%{_datadir}/terminfo/x/xterm-new %{buildroot}%{_datadir}/terminfo/x/xterm

#
# remove unneeded/unwanted files
# have to be done before find commands below
#
rm -f %{buildroot}%{_libdir}/terminfo
%if %{with compat32}
rm -f %{buildroot}%{_prefix}/lib/terminfo
%endif

# fwang: avoid conflict with kon package
rm -f %{buildroot}%{_datadir}/terminfo/k/kon

# bero: Build termcap from the terminfo database
mkdir -p %{buildroot}%{_sysconfdir}
%if ! %cross_compiling
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH %{buildroot}%{_bindir}/tic -Ct misc/terminfo.src > %{buildroot}%{_sysconfdir}/termcap
%else
tic -Ct misc/terminfo.src > %{buildroot}%{_sysconfdir}/termcap
%endif

#
# FIXME
#
(cd %{buildroot} ; find usr/share/terminfo -type d | perl -pe 's||%%dir /|') > %{name}.list
(cd %{buildroot} ; find usr/share/terminfo -not -type d | perl -pe 's||/|') > %{name}-extraterms.list
perl -pe 's||%{_datadir}/terminfo/|' %{SOURCE5} >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}.list"; /^%/ or $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}-extraterms.list

find %{buildroot}/%{_libdir} -name 'lib*.a' -not -type d -not -name "*_g.a" -not -name "*_p.a" -not -name "*w.a" | sed -e "s#^%{buildroot}##" > %{libname}-devel.list

# can't replace directory with symlink (rpm bug), symlink all headers
mkdir %{buildroot}%{_includedir}/ncurses{,w}
for l in %{buildroot}%{_includedir}/*.h; do
    ln -sr $l %{buildroot}%{_includedir}/ncurses
    ln -sr $l %{buildroot}%{_includedir}/ncursesw
done

# Add a few symlinks for legacy compatibility
for i in form menu ncurses panel; do
    ln -s ${i}w.pc %{buildroot}%{_libdir}/pkgconfig/$i.pc
done

# ncurses includes tinfo - let's be compatible with stuff
# that assumes tinfo is a separate library
ln -s ncursesw.pc %{buildroot}%{_libdir}/pkgconfig/tinfo.pc
ln -s libncursesw.so.%{majorminor} %{buildroot}/%{_libdir}/libtinfo.so.%{majorminor}
ln -s libncursesw.so.%{majorminor} %{buildroot}/%{_libdir}/libtinfo.so.%{major}
ln -s libncursesw.so %{buildroot}%{_libdir}/libtinfo.so
ln -s libncursesw.a %{buildroot}%{_libdir}/libtinfo.a
%if %{with compat32}
ln -s libncursesw.so.%{major} %{buildroot}%{_prefix}/lib/libtinfo.so.%{major}
ln -s libncursesw.so.%{major} %{buildroot}%{_prefix}/lib/libtinfo.so
ln -s ncursesw.pc %{buildroot}%{_prefix}/lib/pkgconfig/tinfo.pc
ln -s libncursesw.a %{buildroot}%{_prefix}/lib/libtinfo.a
%endif

# -L/usr/lib64 is harmful
sed -i -e 's,-L%{_libdir} ,,g' %{buildroot}%{_libdir}/pkgconfig/*.pc
%if %{with compat32}
sed -i -e 's,-L%{_prefix}/lib ,,g' %{buildroot}%{_prefix}/lib/pkgconfig/*.pc
%endif

# Prevent weird upgrade failure in which something symlinks libncursesw.so.6 to libtinfo.so.6.3
ln -sf libncursesw.so.%{majorminor} %{buildroot}%{_libdir}/libncursesw.so.%{major}
%if %{with compat32}
ln -sf libncursesw.so.%{majorminor} %{buildroot}%{_prefix}/lib/libncursesw.so.%{major}
%endif

# Binary incompatibilities between ncurses 5 and 6 are small.
# Small enough for this to provide reasonable compatibility with
# some non-free stuff built on prehistoric distros.
ln -s libncurses.so.%{majorminor} %{buildroot}/%{_libdir}/libncurses.so.5
ln -s libtinfo.so.%{majorminor} %{buildroot}/%{_libdir}/libtinfo.so.5

# Don't allow rpm helpers to get rid of that seemingly "wrong" symlink
export DONT_SYMLINK_LIBS=1
export DONT_RELINK=1

# (tpg) do not push our LDFLAGS
sed -i -e 's/%{build_ldflags}//g' %{buildroot}%{_bindir}/ncurses*-config

%files -f %{name}.list
%doc README ANNOUNCE
%{_datadir}/tabset
%{_bindir}/*
%exclude %{_bindir}/ncurses*-config
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%doc %{_mandir}/man7/*

%files -n %{libname}
%{_libdir}/libncurses.so.%{major}*
%{_libdir}/libncurses.so.5
%{_libdir}/libtinfo.so.%{major}*
%{_libdir}/libtinfo.so.5

%files -n %{utf8libname}
%{_libdir}/libncursesw.so.%{major}*

%files extraterms -f %{name}-extraterms.list
%doc README

%files -n %{devname}
%doc doc c++ test
%{_bindir}/ncurses*-config
%{_libdir}/libcurses.so
%{_libdir}/libform.so
%{_libdir}/libformw.so
%{_libdir}/libmenu.so
%{_libdir}/libmenuw.so
%if %{with cplusplus}
%{_libdir}/libncurses++w.so
%{_libdir}/libncurses++.so
%{_libdir}/pkgconfig/ncurses++w.pc
%endif
%{_libdir}/libncurses.so
%{_libdir}/libncursesw.so
%{_libdir}/libpanel.so
%{_libdir}/libpanelw.so
%{_libdir}/libtinfo.so
%{_libdir}/pkgconfig/formw.pc
%{_libdir}/pkgconfig/menuw.pc
%{_libdir}/pkgconfig/ncursesw.pc
%{_libdir}/pkgconfig/panelw.pc
%{_libdir}/pkgconfig/form.pc
%{_libdir}/pkgconfig/menu.pc
%{_libdir}/pkgconfig/ncurses.pc
%{_libdir}/pkgconfig/panel.pc
%{_libdir}/pkgconfig/tinfo.pc
%{_includedir}/*.h
%dir %{_includedir}/ncurses
%{_includedir}/ncurses/*.h
%dir %{_includedir}/ncursesw
%{_includedir}/ncursesw/*.h
%doc %{_mandir}/man3/*

%files -n %{staticname}
%{_libdir}/libcurses.a
%{_libdir}/libform.a
%{_libdir}/libformw.a
%{_libdir}/libmenu.a
%{_libdir}/libmenuw.a
%{_libdir}/libncurses.a
%{_libdir}/libncursesw.a
%{_libdir}/libpanel.a
%{_libdir}/libpanelw.a
%{_libdir}/libtinfo.a
%if %{with cplusplus}
%{_libdir}/libncurses++w.a
%{_libdir}/libncurses++.a
%endif

%files -n termcap
%{_sysconfdir}/termcap

%if %{with compat32}
# 32-bit compat bits
%(for i in ncurses form menu ncurses++ panel tinfo ncursesw formw menuw ncurses++w panelw; do
	if [ "$i" = "ncurses" ]; then
		EXTRA="%{_prefix}/lib/libcurses.so"
		EXTRASTATIC="%{_prefix}/lib/libcurses.a"
	else
		EXTRA=""
		EXTRASTATIC=""
	fi
	cat <<EOF
%package -n lib${i}
Summary: 32-bit compatibility version of the ${i} library
Group: System/Libraries
Obsoletes: lib${i}6 < %{EVRD}
Provides: lib${i}6 = %{EVRD}

%description -n lib${i}
32-bit compatibility version of the ${i} library.

%files -n lib${i}
%{_prefix}/lib/lib${i}.so.6*

%package -n lib${i}-devel
Summary: Development files for the 32-bit version of the ${i} library
Group: Development/C
Requires: lib${i} = %{EVRD}
# Headers are shared between 32-bit and 64-bit versions
Requires: %{devname} = %{EVRD}
Requires: libc6

%description -n lib${i}-devel
Development files for the 32-bit version of the ${i} library.

%files -n lib${i}-devel
%{_prefix}/lib/lib${i}.so
$EXTRA
%{_prefix}/lib/pkgconfig/${i}.pc

%package -n lib${i}-static-devel
Summary: Static library files for the 32-bit version of the ${i} library
Group: Development/C
Requires: lib${i}-devel = %{EVRD}

%description -n lib${i}-static-devel
Static library files for the 32-bit version of the ${i} library.

%files -n lib${i}-static-devel
%{_prefix}/lib/lib${i}.a
$EXTRASTATIC
EOF
done)
%endif

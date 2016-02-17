%define date 20160130
%define major 6
%define majorminor 6.0
%define utf8libname %mklibname %{name}w %{major}
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}
%define utf8devname %mklibname -d %{name}w

%bcond_with uclibc
%bcond_with cplusplus
%bcond_with gpm

# ugly as fuck, but at least mostly harmless to children and animals..
%define libgen()\
%package -n	%2%{_lib}%{1}%{4}\
Summary:	Ncurses %{1} library\
Group:		System/Libraries\
Conflicts:	%{_lib}ncurses%{major} < 5.9-6.20120922.1 \
Conflicts:	%{_lib}ncursesw%{major} < 5.9-6.20120922.1 \
\
%description -n	%2%{_lib}%{1}%{4}\
This package comes with lib%{1} from the ncurses library.\
\
%files -n	%2%{_lib}%{1}%{4}\
%{3}%{_libdir}/lib%{1}.so.%{4}*\
%{nil}

Summary:	A CRT screen handling and optimization package
Name:		ncurses
Version:	6.0
%if "%{date}" != ""
Release:	0.%{date}.5
Source0:	ftp://invisible-island.net/ncurses/current/%{name}-%{version}-%{date}.tgz
%else
Release:	1
Source0:	ftp://invisible-island.net/ncurses/%{name}-%{version}.tar.gz
%endif
License:	MIT
Group:		System/Libraries
Url:		http://www.gnu.org/software/ncurses/ncurses.html
Source4:	ncurses-resetall.sh
Source5:	ncurses-useful-terms
Source6:	ncurses.rpmlintrc
Patch1:		ncurses-5.6-xterm-debian.patch
# Alias "console" to "linux"
Patch2:		ncurses-5.9-20120811-linux-console.patch
Patch3:		ncurses-5.9-buildfix.patch
Patch7:		ncurses-5.9-urxvt.patch
Patch8:		ncurses-5.9-20121208-config-dont-print-standard-lib64-path.patch
%if %{with gpm}
BuildRequires:	gpm-devel
%if %{with uclibc}
BuildRequires:	uclibc-%{lib}gpm-devel
%endif
%endif
BuildRequires:	sharutils
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif
Conflicts:	%{name}-extraterms < 5.9-6.20121026.3

%description
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%if %{with uclibc}
%package -n	uclibc-%{name}
Summary:	Tools for ncurses built against uClibc
Group:		System/Libraries

%description -n	uclibc-%{name}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.
%endif

# to be killed
###############################################################################
%package -n	%{libname}
Summary:	The development files for applications which use ncurses
Group:		System/Libraries

%description -n	%{libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.


%libgen form %{nil} %{nil} %{major}
%libgen menu %{nil} %{nil} %{major}
%libgen panel %{nil} %{nil} %{major}

%libgen formw %{nil} %{nil} %{major}
%libgen menuw %{nil} %{nil} %{major}
%libgen panelw %{nil} %{nil} %{major}

%if %{with uclibc}
%libgen formw uclibc- %{uclibc_root} %{major}
%libgen menuw uclibc- %{uclibc_root} %{major}
%libgen panelw uclibc- %{uclibc_root} %{major}
%libgen tic uclibc- %{uclibc_root} %{major}
%libgen tinfo uclibc- %{uclibc_root} %{major}
%endif

%package -n	%{utf8libname}
Summary:	Ncurses libraries which support UTF8
Group:		System/Libraries

%description -n %{utf8libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

This package contains ncurses libraries which support wide char (UTF8),
and is not compatible with those without.

%if %{with uclibc}
%package -n	uclibc-%{utf8libname}
Summary:	Ncurses libraries which support UTF8 (uClibc linked)
Group:		System/Libraries

%description -n uclibc-%{utf8libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

This package contains ncurses libraries which support wide char (UTF8),
%endif

%package	extraterms
Summary:	Some exotic terminal descriptions
Group:		System/Libraries
BuildArch:	noarch

%description	extraterms
Install the ncurses-extraterms package if you use some exotic terminals.

%if %{with uclibc}
%package -n	uclibc-%{devname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Provides:	uclibc-%{name}-devel = %{EVRD}
Requires:	%{devname} = %{EVRD}
Requires:	uclibc-%{utf8libname} = %{version}
Requires:	uclibc-%{_lib}tic%{major} = %{version}
Requires:	uclibc-%{_lib}tinfo%{major} = %{version}
Requires:	uclibc-%{_lib}formw%{major} = %{version}
Requires:	uclibc-%{_lib}menuw%{major} = %{version}
Requires:	uclibc-%{_lib}panelw%{major} = %{version}
Conflicts:	uclibc-ncurses < 5.9-7.20131123.1
Conflicts:	ncurses < 5.9-8.20150523.2

%description -n	uclibc-%{devname}
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.
%endif

%package -n	%{devname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
# just keep this depdenency for untangling initial dependency issues..
%if "%{_lib}" == "lib64"
Provides:	devel(libncurses(64bit))
%else
Provides:	devel(libncurses)
%endif
Provides:	pkgconfig(ncurses)
Provides:	ncursesw-devel = %{version}-%{release}
Requires:	%{utf8libname} = %{version}
Requires:	%{_lib}formw%{major} = %{version}
Requires:	%{_lib}menuw%{major} = %{version}
Requires:	%{_lib}panelw%{major} = %{version}
# /usr/include/termcap.h conflicts
Conflicts:	termcap-devel > 2.0.8-53
Conflicts:	ncurses < 5.9-7.20131123.1

Obsoletes:	%mklibname -d %name 5
Obsoletes:	%mklibname -d %{name}w 5
Conflicts:	%{_lib}ncurses-devel < 5.7-3.20091128.2
%rename		%{utf8devname}

%description -n	%{devname}
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package -n	termcap
Summary:	The terminal feature database used by certain applications
Group:		System/Libraries
Epoch:		1
BuildArch:	noarch

%description -n	termcap
The termcap package provides the /etc/termcap file.  /etc/termcap is
a database which defines the capabilities of various terminals and
terminal emulators.  Certain programs use the /etc/termcap file to
access various features of terminals (the bell, colors, and graphics,
etc.).

%prep
%if "%{date}" != ""
%setup -q -n %{name}-%{version}-%{date}
%else
%setup -q
%endif

%patch7 -p1 -b .urxvt~

# regenerating configure needs patched autoconf, so modify configure
# directly
%patch1 -p1 -b .deb~
%patch3 -p1 -b .bf~

%patch2 -p1 -b .console~
%patch8 -p1 -b .lib64~

find . -name "*.orig" -o -name "*~" | xargs rm -f
# fix some permissions
chmod 755 c++/edit_cfg.sh test/listused.sh test/configure test/tracemunch

# we don't need nor want this, and it also pulls in a dependency on /usr/bin/make
rm -rf test/package

# FIXME workaround for misdetection when using musl
sed -i -e 's,#if HAVE_GETTTYNAM,#if 0,g' progs/tset.c

%build
export PKG_CONFIG_LIBDIR=%{_libdir}/pkgconfig

CONFIGURE_TOP="$PWD"

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--includedir=%{uclibc_root}%{_includedir} \
	--without-libtool \
	--with-shared \
	--without-normal \
%if %{with cplusplus}
	--with-cxx \
%else
	--without-cxx \
%endif
	--enable-overwrite \
	--without-profile \
%if %{with gpm}
	--with-gpm \
%endif
	--disable-termcap \
	--disable-getcap \
	--enable-const \
	--enable-hard-tabs \
	--enable-hash-map \
	--enable-no-padding \
	--enable-sigwinch \
	--without-ada \
	--enable-widec \
	--enable-xmc-glitch \
	--enable-colorfgbg \
	--disable-pc-files \
	--without-develop \
	--without-cxx-binding \
	--without-tests \
	--with-termlib=tinfo \
	--with-ticlib=tic \
	--disable-tic-depends \
	--enable-ext-colors \
	--enable-ext-mouse \
	--enable-sp-funcs

%make
popd
%endif


# tODO: this should die
mkdir -p ncurses-normal
pushd ncurses-normal
%configure \
	--without-libtool \
	--with-shared \
	--with-normal \
%if %{with cplusplus}
	--with-cxx \
%else
	--without-cxx \
%endif
	--without-debug \
	--enable-overwrite \
	--without-profile \
%if %{with gpm}
	--with-gpm \
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
	--without-progs

%make
popd

mkdir -p ncurses-utf8
pushd ncurses-utf8
%configure \
	--with-pkg-config-libdir=%{_libdir}/pkgconfig \
	--without-libtool \
	--with-shared \
	--with-normal \
%if %{with cplusplus}
	--with-cxx \
%else
	--without-cxx \
%endif
	--without-debug \
	--enable-overwrite \
	--without-profile \
%if %{with gpm}
	--with-gpm \
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
	--enable-sp-funcs
%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
install -d %{buildroot}%{uclibc_root}/%{_lib}
mv %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so.* %{buildroot}%{uclibc_root}/%{_lib}
rm %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so
#ln -sr %{buildroot}%{uclibc_root}/%{_lib}/libncursesw.so.%{majorminor} %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so
cat > %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so << EOF
/* GNU ld script
Just linking against all ncurses libraries as needed...
*/
`%__cc -fuse-ld=bfd    -Wl,--verbose 2>&1 | sed -n '/OUTPUT_FORMAT/,/)/p'`
GROUP ( AS_NEEDED ( %{uclibc_root}/%{_lib}/libncursesw.so.%{majorminor} %{uclibc_root}%{_libdir}/libtinfo.so.%{majorminor} %{uclibc_root}%{_libdir}/libtic.so.%{majorminor}) )
EOF

rm  %{buildroot}%{uclibc_root}%{_libdir}/*.a
%endif

# we only install the libraries for a while untill all our packages has been
# rebuilt against the unicode version and no packages needs this anymore
pushd ncurses-normal
make install.libs DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/lib*.{a,so}
popd

pushd ncurses-utf8
%makeinstall_std
popd

# the resetall script
install -m 755 %{SOURCE4} %{buildroot}%{_bindir}/resetall
# we don't want this in doc
rm -f c++/demo

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libncurses{,w}.so.* %{buildroot}/%{_lib}
rm %{buildroot}%{_libdir}/libncursesw.so
ln -sr %{buildroot}/%{_lib}/libncursesw.so.%{majorminor} %{buildroot}%{_libdir}/libncursesw.so
for i in form menu ncurses panel; do
	ln -s lib${i}w.a %{buildroot}%{_libdir}/lib${i}.a
	ln -s lib${i}w.so %{buildroot}%{_libdir}/lib${i}.so
done
ln -s libncursesw.so %{buildroot}%{_libdir}/libcurses.so
ln -s libncursesw.a %{buildroot}%{_libdir}/libcurses.a
ln -s libncurses++w.a %{buildroot}%{_libdir}/libncurses++.a

#
# FIXME
# OK do not time to debug it now
#
%ifnarch armv7hl
cp %{buildroot}%{_datadir}/terminfo/x/xterm %{buildroot}%{_datadir}/terminfo/x/xterm2
cp %{buildroot}%{_datadir}/terminfo/x/xterm-new %{buildroot}%{_datadir}/terminfo/x/xterm
%endif

#
# remove unneeded/unwanted files
# have to be done before find commands below
#
rm -f %{buildroot}%{_libdir}/terminfo

# fwang: avoid conflict with kon package
rm -f %{buildroot}%{_datadir}/terminfo/k/kon

# bero: Build termcap from the terminfo database
mkdir -p %{buildroot}%_sysconfdir
%if ! %cross_compiling
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_lib}:$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH $RPM_BUILD_ROOT%{_bindir}/tic -Ct misc/terminfo.src > %{buildroot}%{_sysconfdir}/termcap
%else
tic -Ct misc/terminfo.src > %{buildroot}%{_sysconfdir}/termcap
%endif

#
# FIXME
#
(cd %{buildroot} ; find usr/share/terminfo      -type d | perl -pe 's||%%dir /|') > %{name}.list
(cd %{buildroot} ; find usr/share/terminfo -not -type d | perl -pe 's||/|')       > %{name}-extraterms.list
perl -pe 's||%{_datadir}/terminfo/|' %{SOURCE5} >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}.list"; /^%/ or $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}-extraterms.list

find %{buildroot}/%{_libdir} -name 'lib*.a' -not -type d -not -name "*_g.a" -not -name "*_p.a" -not -name "*w.a" | sed -e "s#^%{buildroot}##" > %{libname}-devel.list

# can't replace directory with symlink (rpm bug), symlink all headers
mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
    ln -sr $l $RPM_BUILD_ROOT%{_includedir}/ncurses
    ln -sr $l $RPM_BUILD_ROOT%{_includedir}/ncursesw
done

%multiarch_includes %{buildroot}%{_includedir}/curses.h

%files -f %{name}.list
%doc README ANNOUNCE
%{_datadir}/tabset
%{_bindir}/*
%exclude %{_bindir}/ncurses*-config
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_bindir}/*
%exclude %{uclibc_root}%{_bindir}/ncurses*-config
%endif

%files -n %{libname}
%attr(755,root,root) /%{_lib}/libncurses.so.%{major}*

%files -n %{utf8libname}
%attr(755,root,root) /%{_lib}/libncursesw.so.%{major}*
%optional %attr(755,root,root) %{_libdir}/libncursesw.so.%{major}

%if %{with uclibc}
%files -n uclibc-%{utf8libname}
%attr(755,root,root) %{uclibc_root}/%{_lib}/libncursesw.so.%{major}*
%endif

%files extraterms -f %{name}-extraterms.list
%doc README

%if %{with uclibc}
%files -n uclibc-%{devname}
%{uclibc_root}%{_bindir}/ncurses*-config
%{uclibc_root}%{_libdir}/lib*.so
# not final, but just work around library issues for now..
%{uclibc_root}%{_includedir}/*
%endif

%files -n %{devname}
%doc doc c++ test
%{_bindir}/ncurses*-config
%{_libdir}/libcurses.a
%{_libdir}/libcurses.so
%{_libdir}/libform.a
%{_libdir}/libform.so
%{_libdir}/libformw.a
%{_libdir}/libformw.so
%{_libdir}/libmenu.a
%{_libdir}/libmenu.so
%{_libdir}/libmenuw.a
%{_libdir}/libmenuw.so
%{_libdir}/libncurses++.a
%if %{with cplusplus}
%{_libdir}/libncurses++w.a
%{_libdir}/pkgconfig/ncurses++w.pc
%endif
%{_libdir}/libncurses.a
%{_libdir}/libncurses.so
%{_libdir}/libncursesw.a
%{_libdir}/libncursesw.so
%{_libdir}/libpanel.a
%{_libdir}/libpanel.so
%{_libdir}/libpanelw.a
%{_libdir}/libpanelw.so
%{_libdir}/pkgconfig/formw.pc
%{_libdir}/pkgconfig/menuw.pc
%{_libdir}/pkgconfig/ncursesw.pc
%{_libdir}/pkgconfig/panelw.pc
%{_includedir}/*.h
%optional %{_includedir}/multiarch-*/curses.h
%dir %{_includedir}/ncurses
%{_includedir}/ncurses/*.h
%dir %{_includedir}/ncursesw
%{_includedir}/ncursesw/*.h
%{_mandir}/man3/*

%files -n termcap
%{_sysconfdir}/termcap

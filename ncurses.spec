%define date		20120922
%define	major		5
%define	majorminor	5.9
%define utf8libname	%mklibname %{name}w %{major}
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname -d %{name}
%define utf8devname	%mklibname -d %{name}w

%bcond_without	uclibc

Summary:	A CRT screen handling and optimization package
Name:		ncurses
Version:	5.9
Release:	6.%{date}.1
License:	MIT
Group:		System/Libraries
Url:		http://www.gnu.org/software/ncurses/ncurses.html
Source0:	ftp://invisible-island.net/ncurses/current/%{name}-%{version}-%{date}.tgz
Source4:	ncurses-resetall.sh
Source5:    	ncurses-useful-terms
Patch1:		ncurses-5.6-xterm-debian.patch
# Alias "console" to "linux"
Patch2:		ncurses-5.9-20120811-linux-console.patch
Patch7:		ncurses-5.9-urxvt.patch
BuildRequires:	gpm-devel
BuildRequires:	sharutils
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-9
%endif
Conflicts:	%{name}-extraterms < 5.6-1.20070721.1

%description
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package -n	uclibc-%{name}
Summary:	Tools for ncurses built against uClibc
Group:		System/Libraries

%description -n	uclibc-%{name}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package -n	%{libname}
Summary:	The development files for applications which use ncurses
Group:		System/Libraries
Requires:	ncurses = %{version}-%{release}

%description -n	%{libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package -n	%{utf8libname}
Summary:	Ncurses libraries which support UTF8
Group:		System/Libraries
Requires:	ncurses = %{version}-%{release}

%description -n %{utf8libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

This package contains ncurses libraries which support wide char (UTF8),
and is not compatible with those without.

%package -n	uclibc-%{utf8libname}
Summary:	Ncurses libraries which support UTF8 (uClibc linked)
Group:		System/Libraries
Requires:	ncurses = %{version}-%{release}

%description -n uclibc-%{utf8libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

This package contains ncurses libraries which support wide char (UTF8),
and is not compatible with those without.

%package	extraterms
Summary:	Some exotic terminal descriptions
Group:		System/Libraries
Requires:	ncurses = %{version}-%{release}

%description	extraterms
Install the ncurses-extraterms package if you use some exotic terminals.

%package -n	%{devname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname -d %name 5

%description -n	%{devname}
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package -n	%{utf8devname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Requires:	%{utf8libname} = %{version}-%{release}
Provides:	ncursesw-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name}w 5
Conflicts:	%{_lib}ncurses-devel < 5.7-3.20091128.2

%description -n	%{utf8devname}
The libraries for developing applications that use ncurses CRT screen
handling and optimization package. Install it if you want to develop
applications which will use ncurses.

Note that the libraries included here supports wide char (UTF-8),
and is not compatible with those without. When linking programs with
these libraries, you will have to append a "w" to the library names,
i.e. -lformw, -lmenuw, -lncursesw, -lpanelw.

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
%setup -q -n %{name}-%{version}-%{date}

%patch7 -p1 -b .urxvt~

# regenerating configure needs patched autoconf, so modify configure
# directly
%patch1 -p1 -b .deb

%patch2 -p1 -b .console~

find . -name "*.orig" -o -name "*~" | xargs rm -f
# fix some permissions
chmod 755 c++/edit_cfg.sh test/listused.sh test/configure test/tracemunch

# we don't need nor want this, and it also pulls in a dependency on /usr/bin/make
rm -rf test/package

%build
export PKG_CONFIG_LIBDIR=%{_libdir}/pkgconfig

CONFIGURE_TOP=$PWD

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%configure2_5x \
	CC=%{uclibc_cc} \
	CFLAGS="%{uclibc_cflags}" \
	--includedir=%{uclibc_root}%{_includedir} \
	--without-libtool \
	--with-shared \
	--without-normal \
	--with-cxx \
	--enable-overwrite \
	--without-profile \
	--without-gpm \
	--enable-termcap \
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
	--with-ospeed=unsigned \
	--without-develop \
	--without-cxx-binding \
	--without-tests \
	--libdir=%{uclibc_root}%{_libdir} \
	--bindir=%{uclibc_root}%{_bindir}

%make
popd
%endif

mkdir -p ncurses-normal
pushd ncurses-normal
%configure2_5x \
	--includedir=%{_includedir}/ncurses \
	--with-pkg-config-libdir=%{_libdir}/pkgconfig \
	--without-libtool \
	--with-shared \
	--with-normal \
	--with-cxx \
	--without-debug \
	--enable-overwrite \
	--without-profile \
	--with-gpm \
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
	--enable-pc-files \
	--with-ospeed=unsigned

%make
popd

mkdir -p ncurses-utf8
pushd ncurses-utf8
%configure2_5x \
	--includedir=%{_includedir}/ncursesw \
	--with-pkg-config-libdir=%{_libdir}/pkgconfig \
	--without-libtool \
	--with-shared \
	--with-normal \
	--with-cxx \
	--without-debug \
	--enable-overwrite \
	--without-profile \
	--with-gpm \
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
	--with-ospeed=unsigned

%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
install -d %{buildroot}%{uclibc_root}/%{_lib}
mv %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so.* %{buildroot}%{uclibc_root}/%{_lib}
rm -f %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so
ln -sr %{buildroot}%{uclibc_root}/%{_lib}/libncursesw.so.%{majorminor} %{buildroot}%{uclibc_root}%{_libdir}/libncursesw.so
rm -f %{buildroot}%{uclibc_root}%{_libdir}/*.a
%endif

pushd ncurses-utf8
%makeinstall_std
popd

pushd ncurses-normal
%makeinstall_std
popd

ln -sf ncurses/curses.h %{buildroot}/usr/include/ncurses.h
for I in curses unctrl eti form menu panel term; do
	ln -sf ncurses/$I.h %{buildroot}/usr/include/$I.h
done

# the resetall script
install -m 755 %{SOURCE4} %{buildroot}%{_bindir}/resetall
# we don't want this in doc
rm -f c++/demo

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libncurses.so* %{buildroot}/%{_lib}
ln -s /%{_lib}/libncurses.so.%{majorminor} %{buildroot}%{_libdir}/libncurses.so.%{majorminor}
ln -s /%{_lib}/libncurses.so.%{majorminor} %{buildroot}%{_libdir}/libncurses.so.%{major}
ln -s /%{_lib}/libncurses.so.%{majorminor} %{buildroot}%{_libdir}/libncurses.so

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

# fwang: avoid conflict with kon package
rm -f %{buildroot}%{_datadir}/terminfo/k/kon

# bero: Build termcap from the terminfo database
mkdir -p %{buildroot}%_sysconfdir
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_lib}:$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH $RPM_BUILD_ROOT%{_bindir}/tic -Ct misc/terminfo.src > %{buildroot}%{_sysconfdir}/termcap

#
# FIXME
#
(cd %{buildroot} ; find usr/share/terminfo      -type d | perl -pe 's||%%dir /|') > %{name}.list
(cd %{buildroot} ; find usr/share/terminfo -not -type d | perl -pe 's||/|')       > %{name}-extraterms.list
perl -pe 's||%{_datadir}/terminfo/|' %{SOURCE5} >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}.list"; /^%/ or $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}-extraterms.list

find %{buildroot}/%{_libdir} -name 'lib*.a' -not -type d -not -name "*_g.a" -not -name "*_p.a" -not -name "*w.a" | sed -e "s#^%{buildroot}##" > %{libname}-devel.list

%multiarch_includes %{buildroot}%{_includedir}/ncurses/curses.h

%multiarch_includes %{buildroot}%{_includedir}/ncursesw/curses.h

%files -f %{name}.list
%doc README ANNOUNCE
%{_datadir}/tabset
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_bindir}/*
%endif

%files -n %{libname}
%attr(755,root,root) /%{_lib}/libncurses.so.*
%attr(755,root,root) %{_libdir}/libform.so.*
%attr(755,root,root) %{_libdir}/libmenu.so.*
%attr(755,root,root) %{_libdir}/libncurses.so.*
%attr(755,root,root) %{_libdir}/libpanel.so.*

%files -n %{utf8libname}
%attr(755,root,root) %{_libdir}/lib*w.so.*

%if %{with uclibc}
%files -n uclibc-%{utf8libname}
%defattr(755,root,root)
%{uclibc_root}/%{_lib}/libncursesw.so.*
%{uclibc_root}%{_libdir}/lib*w.so.*
%endif

%files extraterms -f %{name}-extraterms.list
%doc README

%files -n %{devname}
%doc doc c++ test
/%{_lib}/libncurses.so
%{_libdir}/libcurses.a
%{_libdir}/libcurses.so
%{_libdir}/libform.a
%{_libdir}/libform.so
%{_libdir}/libmenu.a
%{_libdir}/libmenu.so
%{_libdir}/libncurses++.a
%{_libdir}/libncurses.a
%{_libdir}/libncurses.so
%{_libdir}/libpanel.a
%{_libdir}/libpanel.so
%{_libdir}/pkgconfig/form.pc
%{_libdir}/pkgconfig/menu.pc
%{_libdir}/pkgconfig/ncurses++.pc
%{_libdir}/pkgconfig/ncurses.pc
%{_libdir}/pkgconfig/panel.pc
%{_includedir}/ncurses
%{multiarch_includedir}/ncurses
%{_includedir}/*.h
%{_mandir}/man3/*
%if %{with uclibc}
%{uclibc_root}%{_libdir}/lib*.so
# not final, but just work around library issues for now..
%{uclibc_root}%{_includedir}/*
%endif

%files -n %{utf8devname}
%{_includedir}/ncursesw
%{_libdir}/pkgconfig/*w.pc
%{multiarch_includedir}/ncursesw
%{_libdir}/lib*w.so
%{_libdir}/lib*w.a

%files -n termcap
%{_sysconfdir}/termcap

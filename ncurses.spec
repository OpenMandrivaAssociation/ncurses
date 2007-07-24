%define rolluppatch 20070714
%define patchdate 20070721
%define version 5.6
%define release %mkrel 1.%{patchdate}.1
%define major 5
%define majorminor 5.6
%define utf8libname %mklibname %{name}w %{major}
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%define utf8develname %mklibname -d %{name}w

Summary:	A CRT screen handling and optimization package
Name:		ncurses
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
Url:		http://www.gnu.org/software/ncurses/ncurses.html
Source0:	ftp://ftp.gnu.org/gnu/ncurses/%{name}-%{version}.tar.bz2
Source4:	ncurses-resetall.sh
Source5:    	ncurses-usefull-terms
# fwang: Source 100 is rollup patches from
# ftp://invisible-island.net/ncurses/5.6/
Source100:	ncurses-%{version}-%{rolluppatch}-patch.sh

Patch1:		ncurses-5.6-xterm-debian.patch
Patch4:		ncurses-5.3-parallel.patch
Patch5:		ncurses-5.3-utf8.patch
#Patch6:		ncurses-5.4-20041204-remove-extra-dep.patch.bz2 
#Patch8:		ncurses-5.4-deps.patch.bz2

# Patch >100 from here:
# ftp://invisible-island.net/ncurses/5.6/
Patch101:	ncurses-5.6-20070716.patch.gz
Patch102:	ncurses-5.6-20070721.patch.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gpm-devel sharutils
Conflicts:	%{name}-extraterms < 5.6-1.20070721.1

%description
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package -n	%{libname}
Summary:	The development files for applications which use ncurses
Requires:	ncurses
Group:		System/Libraries

%description -n	%{libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package -n	%{utf8libname}
Summary:	Ncurses libraries which support UTF8
Requires:	ncurses
Group:		System/Libraries

%description -n	%{utf8libname}
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

%package -n	%{develname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{libname}-devel
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{libname}-devel
Obsoletes:	%{name}-devel

%description -n	%{develname}
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package -n	%{utf8develname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Requires:	%{utf8libname} = %{version}-%{release}
Provides:	lib%{name}w-devel = %{version}-%{release}
Provides:	%{utf8libname}-devel
Obsoletes:	%{utf8libname}-devel

%description -n	%{utf8develname}
The libraries for developing applications that use ncurses CRT screen
handling and optimization package. Install it if you want to develop
applications which will use ncurses.

Note that the libraries included here supports wide char (UTF-8),
and is not compatible with those without. When linking programs with
these libraries, you will have to append a "w" to the library names,
i.e. -lformw, -lmenuw, -lncursesw, -lpanelw.

%prep
%setup -q

# Let's apply rollup patches at first
cp %SOURCE100 .
/bin/sh ncurses-%{version}-%{rolluppatch}-patch.sh
# Then the official patch
%patch101 -p1
%patch102 -p1

#%patch4 -p1 -b .parallel
%patch5 -p1 -b .utf8

# regenerating configure needs patched autoconf, so modify configure
# directly
#%patch6 -p1 -b .removedep
#%patch7 -p1
#%patch8 -p1 -b .deps
%patch1 -p1 -b .deb

find . -name "*.orig" | xargs rm -f
# fix some permissions
chmod 755 c++/edit_cfg.sh test/listused.sh test/configure test/tracemunch

%build
#OPT_FLAGS="$RPM_OPT_FLAGS -DPURE_TERMINFO -fno-omit-frame-pointer"
#CFLAGS="$OPT_FLAGS -DSVR4_CURSES"
#CXXFLAGS="$OPT_FLAGS"

mkdir -p ncurses-normal
pushd ncurses-normal
CONFIGURE_TOP=.. 
%configure2_5x \
	--includedir=%{_includedir}/ncurses \
	--with-normal --with-shared --without-debug --without-profile \
	--with-gpm --enable-termcap --enable-getcap \
	--enable-const --enable-hard-tabs --enable-hash-map \
	--enable-no-padding --enable-sigwinch --without-ada \
	--enable-xmc-glitch --enable-colorfgbg --with-ospeed=unsigned

%make -j1
popd

mkdir -p ncurses-utf8
pushd ncurses-utf8
CONFIGURE_TOP=.. 
%configure2_5x \
	--includedir=%{_includedir}/ncursesw \
	--with-normal --with-shared --without-debug --without-profile \
	--with-gpm --enable-termcap --enable-getcap \
	--enable-const --enable-hard-tabs --enable-hash-map \
	--enable-no-padding --enable-sigwinch --without-ada \
	--enable-widec --enable-xmc-glitch --enable-colorfgbg --with-ospeed=unsigned

%make -j1
popd

%install
rm -rf $RPM_BUILD_ROOT

pushd ncurses-utf8
%{makeinstall_std}
popd

pushd ncurses-normal
%{makeinstall_std}
popd

ln -sf ../l/linux $RPM_BUILD_ROOT%{_datadir}/terminfo/c/console
ln -sf ncurses/curses.h $RPM_BUILD_ROOT/usr/include/ncurses.h
for I in curses unctrl eti form menu panel term; do
	ln -sf ncurses/$I.h $RPM_BUILD_ROOT/usr/include/$I.h
done

# the resetall script
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/resetall
# we don't want this in doc
rm -f c++/demo

mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libncurses.so* $RPM_BUILD_ROOT/%{_lib}
ln -s /%{_lib}/libncurses.so.%{majorminor} $RPM_BUILD_ROOT%{_libdir}/libncurses.so.%{majorminor}
ln -s /%{_lib}/libncurses.so.%{majorminor} $RPM_BUILD_ROOT%{_libdir}/libncurses.so.%{major}
ln -s /%{_lib}/libncurses.so.%{majorminor} $RPM_BUILD_ROOT%{_libdir}/libncurses.so

#
# FIXME
# OK do not time to debbug it now
#
cp $RPM_BUILD_ROOT%{_datadir}/terminfo/x/xterm $RPM_BUILD_ROOT%{_datadir}/terminfo/x/xterm2
cp $RPM_BUILD_ROOT%{_datadir}/terminfo/x/xterm-new $RPM_BUILD_ROOT%{_datadir}/terminfo/x/xterm

#
# remove unneeded/unwanted files
# have to be done before find commands below
#
rm -f $RPM_BUILD_ROOT%{_libdir}/terminfo

#
# FIXME
#
(cd $RPM_BUILD_ROOT ; find usr/share/terminfo      -type d | perl -pe 's||%%dir /|') > %{name}.list
(cd $RPM_BUILD_ROOT ; find usr/share/terminfo -not -type d | perl -pe 's||/|')       > %{name}-extraterms.list
perl -pe 's||%{_datadir}/terminfo/|' %{SOURCE5} >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}.list"; /^%/ or $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}-extraterms.list

find $RPM_BUILD_ROOT/%{_libdir} -name 'lib*.a' -not -type d -not -name "*_g.a" -not -name "*_p.a" -not -name "*w.a" | sed -e "s#^$RPM_BUILD_ROOT##" > %{libname}-devel.list

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post -n %{utf8libname} -p /sbin/ldconfig

%postun -n %{utf8libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.list
%defattr(-,root,root)
%doc README ANNOUNCE
%{_datadir}/tabset
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files -n %{libname}
%defattr(-,root,root)
%attr(755,root,root) /%{_lib}/lib*.so.*
%attr(755,root,root) %{_libdir}/lib*.so.*
%exclude %{_libdir}/lib*w.so.*

%files -n %{utf8libname}
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/lib*w.so.*

%files extraterms -f %{name}-extraterms.list
%defattr(-,root,root)
%doc README

%files -n %{develname} -f %libname-devel.list
%defattr(-,root,root)
%doc doc c++ test
/%{_lib}/lib*.so
%{_libdir}/lib*.so
%exclude %{_libdir}/lib*w.so
%{_includedir}/ncurses
%{_includedir}/*.h
%{_mandir}/man3/*

%files -n %{utf8develname}
%defattr(-,root,root)
%{_includedir}/ncursesw
%{_libdir}/lib*w.so
%{_libdir}/lib*w.a

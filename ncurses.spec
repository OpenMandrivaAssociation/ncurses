%define rolluppatch 20100424
%define patchdate 20100925
%define version 5.7
%define release %mkrel 5.%{patchdate}.1
%define major 5
%define majorminor 5.7
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
Source0:	ftp://ftp.gnu.org/gnu/ncurses/%{name}-%{version}.tar.gz
Source4:	ncurses-resetall.sh
Source5:    	ncurses-usefull-terms
# fwang: Source 100 is rollup patches from
# ftp://invisible-island.net/ncurses/5.7/
Source100:	ncurses-%{version}-%{rolluppatch}-patch.sh.bz2
Patch1:		ncurses-5.6-xterm-debian.patch
Patch4:		ncurses-5.3-parallel.patch
Patch5:		ncurses-5.3-utf8.patch
Patch6:		ncurses-5.7-format_not_a_string_literal_and_no_format_arguments.diff
Patch7:		ncurses-5.7-urxvt.patch
# Patch >100 from here:
# ftp://invisible-island.net/ncurses/5.7/
Patch101:	ncurses-5.7-20100501.patch.gz
Patch102:	ncurses-5.7-20100515.patch.gz
Patch103:	ncurses-5.7-20100522.patch.gz
Patch104:	ncurses-5.7-20100529.patch.gz
Patch105:	ncurses-5.7-20100605.patch.gz
Patch106:	ncurses-5.7-20100612.patch.gz
Patch107:	ncurses-5.7-20100619.patch.gz
Patch108:	ncurses-5.7-20100626.patch.gz
Patch109:	ncurses-5.7-20100703.patch.gz
Patch110:	ncurses-5.7-20100717.patch.gz
Patch111:	ncurses-5.7-20100724.patch.gz
Patch112:	ncurses-5.7-20100731.patch.gz
Patch113:	ncurses-5.7-20100807.patch.gz
Patch114:	ncurses-5.7-20100814.patch.gz
Patch115:	ncurses-5.7-20100828.patch.gz
Patch116:	ncurses-5.7-20100904.patch.gz
Patch117:	ncurses-5.7-20100911.patch.gz
Patch118:	ncurses-5.7-20100918.patch.gz
Patch119:	ncurses-5.7-20100925.patch.gz
BuildRequires:	gpm-devel
BuildRequires:	sharutils
Conflicts:	%{name}-extraterms < 5.6-1.20070721.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package -n %{libname}
Summary:	The development files for applications which use ncurses
Group:		System/Libraries
Requires:	ncurses = %{version}-%{release}

%description -n %{libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package -n %{utf8libname}
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

%package extraterms
Summary:	Some exotic terminal descriptions
Group:		System/Libraries
Requires:	ncurses = %{version}-%{release}

%description extraterms
Install the ncurses-extraterms package if you use some exotic terminals.

%package -n %{develname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname -d %name 5

%description -n %{develname}
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package -n %{utf8develname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Requires:	%{utf8libname} = %{version}-%{release}
Provides:	lib%{name}w-devel = %{version}-%{release}
Provides:	ncursesw-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name}w 5
Conflicts:	%{_lib}ncurses-devel < 5.7-3.20091128.2

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
bunzip2 -kc %SOURCE100 >./ncurses-%{version}-%{rolluppatch}-patch.sh
/bin/sh ncurses-%{version}-%{rolluppatch}-patch.sh
# Then the official patch
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
#patch4 -p1 -b .parallel

%patch5 -p1 -b .utf8
#%patch6 -p0 -b .format_not_a_string_literal_and_no_format_arguments
%patch7 -p0 -b .urxvt

# regenerating configure needs patched autoconf, so modify configure
# directly
%patch1 -p1 -b .deb

find . -name "*.orig" | xargs rm -f
# fix some permissions
chmod 755 c++/edit_cfg.sh test/listused.sh test/configure test/tracemunch

%build
export PKG_CONFIG_LIBDIR=%{_libdir}/pkgconfig

mkdir -p ncurses-normal
pushd ncurses-normal
CONFIGURE_TOP=.. 
%configure2_5x \
	--includedir=%{_includedir}/ncurses \
	--without-libtool \
	--with-shared \
	--with-normal \
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

%make -j1
popd

mkdir -p ncurses-utf8
pushd ncurses-utf8
CONFIGURE_TOP=.. 
%configure2_5x \
	--includedir=%{_includedir}/ncursesw \
	--without-libtool \
	--with-shared \
	--with-normal \
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

%make -j1
popd

%install
rm -rf %{buildroot}

pushd ncurses-utf8
%{makeinstall_std}
popd

pushd ncurses-normal
%{makeinstall_std}
popd

ln -sf ../l/linux %{buildroot}%{_datadir}/terminfo/c/console
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
# OK do not time to debbug it now
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

#
# FIXME
#
(cd %{buildroot} ; find usr/share/terminfo      -type d | perl -pe 's||%%dir /|') > %{name}.list
(cd %{buildroot} ; find usr/share/terminfo -not -type d | perl -pe 's||/|')       > %{name}-extraterms.list
perl -pe 's||%{_datadir}/terminfo/|' %{SOURCE5} >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}.list"; /^%/ or $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}-extraterms.list

find %{buildroot}/%{_libdir} -name 'lib*.a' -not -type d -not -name "*_g.a" -not -name "*_p.a" -not -name "*w.a" | sed -e "s#^%{buildroot}##" > %{libname}-devel.list

%multiarch_includes %{buildroot}%{_includedir}/ncurses*/curses.h

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{utf8libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{utf8libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

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
%{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/lib*w.so
%exclude %{_libdir}/pkgconfig/*w.pc
%{_includedir}/ncurses
%multiarch %_includedir/multiarch*/ncurses
%{_includedir}/*.h
%{_mandir}/man3/*

%files -n %{utf8develname}
%defattr(-,root,root)
%{_includedir}/ncursesw
%{_libdir}/pkgconfig/*w.pc
%multiarch %_includedir/multiarch*/ncursesw
%{_libdir}/lib*w.so
%{_libdir}/lib*w.a

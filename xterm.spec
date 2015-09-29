Summary:	The standard terminal emulator for the X Window System
Name:		xterm
Version:	320
Release:	2
License:	MIT
Group:		Terminals
Url:		http://invisible-island.net/xterm/
Source0:	ftp://invisible-island.net/xterm/%{name}-%{version}.tgz
Source9:	%{name}.desktop
Source10:	failsafe.desktop
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
# from http://www.vim.org/scripts/script.php?script_id=1349, public domain
Source20:	colortest.pl
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	luit
Requires:	luit
Requires(post,postun):	update-alternatives

%description
The XTerm program is the standard terminal emulator for the X Window System. It
provides DEC VT102/VT220 and Tektronix 4014 compatible terminals for programs
that can't use the window system directly. If the underlying operating system
supports terminal resizing capabilities (for example, the SIGWINCH signal in
systems derived from 4.3bsd), xterm will use the facilities to notify programs
running in the window whenever it is resized.

The xterm included in this package has support for 256 colors enabled.

%prep
%setup -q
cp %{SOURCE20} .

%build
%configure \
   --disable-full-tgetent \
   --enable-wide-chars \
   --x-includes=%{_includedir}/freetype2 \
   --enable-luit \
   --enable-256-color \
   --with-app-defaults=%{_libdir}/X11/app-defaults \
   --with-icon-theme=hicolor \
   --with-icondir=%{_iconsdir}

%make

%install
%makeinstall_std

# NOTE: encodingMode: locale means to follow the charset encoding of the
# locale. A quite complete unicode font is set as the default (instead of the
# very poor "fixed" one). a quick cat is used instead of patching the sources;
# it shoulmd be made the default imho
# locale: true means to use luit to convert locale encoding to unicode
# for display.
# luit support is needed for it to work -- pablo
cat << EOF >> %{buildroot}%{_libdir}/X11/app-defaults/XTerm

*.vt100.font: -misc-fixed-medium-r-normal--15-140-75-75-c-90-iso10646-1
*.vt100.encodingMode: locale
*.locale: true
*.PtyInitialErase: on
*.backarrowKeyIsErase: on
*.allowFontOps: false
*.allowTcapOps: false
*.disallowedWindowOps: 1,2,3,4,5,6,7,8,9,11,13,14,18,19,20,21,GetSelection,SetSelection,SetWinLines,SetXprop
EOF

# (tpg) install desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE9} %{buildroot}%{_datadir}/applications/%{name}.desktop

# (tpg) use xterm as failsafe for xsession
mkdir -p %{buildroot}%{_datadir}/xsessions
install -m 644 %{SOURCE10} %{buildroot}%{_datadir}/xsessions/failsafe.desktop

for xpm in xterm{-color_32x32,-color_48x48,_32x32,_48x48}.xpm; do
	rm -f %{buildroot}%{_datadir}/pixmaps/$xpm
done
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{SOURCE11} \
	%{buildroot}%{_iconsdir}/hicolor/16x16/apps/xterm-terminal.png
install -m 644 %{SOURCE12} \
	%{buildroot}%{_iconsdir}/hicolor/32x32/apps/xterm-terminal.png
install -m 644 %{SOURCE13} \
	%{buildroot}%{_iconsdir}/hicolor/48x48/apps/xterm-terminal.png

%post
update-alternatives --install %{_bindir}/xvt xvt %{_bindir}/xterm 18 || :

%postun
[[ "$1" = "0" ]] && update-alternatives --remove xvt %{_bindir}/xterm || :

%files
%doc ctlseqs.txt colortest.pl
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/X11/app-defaults/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/xsessions/failsafe.desktop
%{_iconsdir}/hicolor/*/apps/xterm-terminal.png
%{_datadir}/pixmaps/*.xpm

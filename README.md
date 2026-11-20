# Always Blank Tab

A tiny browser extension that keeps an empty **New Tab** at the far right of every window.
Click it, type your search, and a fresh blank tab appears next to it — so there is always one ready.

Works in Brave, Chrome, Edge and other Chromium-based browsers (Manifest V3).

[Türkçe açıklama aşağıda ↓](#türkçe)

## How it works

- If the rightmost tab is not an empty New Tab, the extension adds one in the background (it does not steal focus).
- When you type into that blank tab, it becomes a normal tab and a new blank tab is added after it.
- If you already have an unused blank tab elsewhere (e.g. from `Ctrl+T`), it is moved to the end instead of creating another one, so blank tabs don't pile up.
- Links opened from a page land to the left of the blank tab.
- While you are dragging a tab, the extension waits and retries after you drop it.

## Install

1. Download this repository (**Code → Download ZIP**) and extract it.
2. Open `brave://extensions` (or `chrome://extensions`, `edge://extensions`).
3. Turn on **Developer mode**.
4. Click **Load unpacked** and select the folder that contains `manifest.json`.
   On Windows, extracting may create a nested folder like `always-blank-tab-main\always-blank-tab-main` — pick the inner one.

Private/incognito windows are not affected unless you enable **Allow in Incognito** on the extension's details page.

## Permissions

Only `tabs` — needed to see which tab is a blank New Tab. No data is collected or sent anywhere; there is no network code.

## Test checklist

| # | Action | Expected |
|---|---|---|
| 1 | Open the browser | A blank tab sits on the far right |
| 2 | Type a search into it | Search opens there; a new blank tab appears to its right |
| 3 | Click the blank tab, type nothing, switch away | Nothing changes |
| 4 | `Ctrl+T`, then search in that tab | The old blank tab moves to the end; still only one |
| 5 | Middle-click a link | It opens left of the blank tab |
| 6 | Close the blank tab | A new one appears |
| 7 | Close every other tab | Window stays open with the blank tab |
| 8 | Drag a tab to the right of the blank tab | After dropping, the blank tab returns to the end |
| 9 | Drag a tab out into a new window / `Ctrl+N` | Each window gets its own blank tab |
| 10 | Pin a tab | Pinned tab goes left, blank tab stays right |
| 11 | Restart the browser with session restore | Exactly one blank tab on the right |

## License

[MIT](LICENSE)

---

## Türkçe

Her pencerenin en sağında her zaman boş bir **Yeni Sekme** tutan küçük bir tarayıcı eklentisi.
Boş sekmeye tıklayıp bir şey aratınca, sağına hemen yeni bir boş sekme açılır; böylece hep bir tane hazır bekler.

Brave, Chrome, Edge ve diğer Chromium tabanlı tarayıcılarda çalışır.

### Nasıl çalışır

- En sağdaki sekme boş değilse arka planda yeni bir boş sekme ekler (o sekmeye geçirmez).
- Boş sekmeye bir şey yazınca o sekme normal sekme olur ve sağına yeni bir boş sekme gelir.
- Başka bir yerde kullanılmayan boş sekme varsa (ör. `Ctrl+T` ile açılmış), yenisini açmak yerine onu sona taşır; boş sekmeler birikmez.
- Sayfalardan açılan linkler boş sekmenin soluna açılır.
- Sekme sürüklerken araya girmez, bıraktıktan sonra tekrar dener.

### Kurulum

1. Bu repoyu indir (**Code → Download ZIP**) ve zip'ten çıkar.
2. Adres çubuğuna `brave://extensions` yaz (Chrome'da `chrome://extensions`).
3. **Geliştirici modu**nu aç.
4. **Paketlenmemiş öğe yükle** ile içinde `manifest.json` olan klasörü seç.
   Windows'ta klasör iç içe çıkabilir; içteki klasörü seç.

Gizli pencerelerde varsayılan olarak çalışmaz; istersen eklentinin ayrıntılar sayfasından **Gizli modda izin ver**'i aç.

### İzinler

Sadece `tabs` izni kullanılır (hangi sekmenin boş olduğunu görmek için). Hiçbir veri toplanmaz veya gönderilmez.

### Lisans

[MIT](LICENSE)

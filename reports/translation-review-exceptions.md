# Translation Review Exceptions

These files are still flagged by `translation-file-map.csv` only because the scanner decodes Chinese text inside Markdown link targets or remote asset names. They do not contain remaining Chinese filenames, headings, Markdown body text, or code comments.

| File | Reason Flagged | Why No Change Is Needed |
| --- | --- | --- |
| `notes/HTTP.md` | Remote image URL contains `_u4E0B_u8F7D.png`, an encoded asset filename that decodes to a Chinese word meaning "download". | The link points to an external hosted asset. There is no untranslated repository content or local filename to migrate. |
| `notes/Linux.md` | Reference links include URL-encoded Chinese text in external URLs, including one blog slug and one Chinese Wikipedia article path. | These are external references. The visible link text is already English, and the repository has no broken internal link or untranslated body text here. |
| `notes/MySQL.md` | Reference link to a Chinese Wikipedia article has URL-encoded Chinese in the target path. | This is an external reference URL. The visible link text is already English, and no repository content needs translation. |
| `notes/attack-techniques.md` | Reference links to Chinese Wikipedia articles for security topics have URL-encoded Chinese in the target paths. | These are external reference URLs. The visible link text is already English, and no internal navigation or source content is affected. |
| `notes/caching.md` | Reference link to a Chinese Wikipedia article has URL-encoded Chinese in the target path. | This is an external reference URL. The visible link text is already English, and no repository content needs translation. |
| `notes/distributed-systems.md` | External blog URL contains a URL-encoded Chinese path segment for "distributed systems". | This is an external reference URL. Changing it could break the citation, and there is no untranslated repository content. |
| `notes/java-collections.md` | External blog URL contains a URL-encoded Chinese path segment for a Java collections HashMap article. | This is an external reference URL. The visible link text is already English, and no source content or internal link needs migration. |

No changes are required for these review flags unless the project later decides to replace Chinese-language external references with English-language alternatives.

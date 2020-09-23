# wordpress_class_wp_cache_virus_patch

A patch for a virus that creates a file index.php in many folders with the WPPluginsOptions class, the .class-wp-cache.php file with the WPCacheExist class and hidden files with the name of parent directories, which is included in infected plugin files, etc

The script deletes all unnecessary files created by the virus and patches files damaged by the virus.

The virus may be deleting content from wp-load.php if the file is not deleted, then check for this if: 
'''
if( !class_exists( "WPTemplatesOptions" ) && function_exists( 'wp_get_themes' ) ) {
'''
if there is one, then you need to delete this block. 

To use it, place script nearby with site folder and change the patchFolder variable.
After execute: python cleanup.py

IMPORTANT: MAKE A BACKUP BEFORE USING


-------


Патч для вируса который создает во многих папках файл index.php с классом WPPluginsOptions, файл .class-wp-cache.php c классом WPCacheExist и скрытые файлами с названием родитительских каталогов, который инклудится в зараженных файлах плагинов и т.д

Скрипт удаляет все лишние файлы, которые создает вирус и патчит поврежденные вирусом файлы.

Вирус, возможно, удаляет контент из wp-load.php, если файл не удален, то небходимо вручну проверить наличие данного if: 
'''
if( !class_exists( "WPTemplatesOptions" ) && function_exists( 'wp_get_themes' ) ) {
'''
если он есть, то необхоидмо удалить  этот блок 

Для использования поместите файл рядом с папкой сайта и поменяйте patchFolder переменную.
Затем выполните python cleanup.py

ВАЖНО: ПЕРЕД ИСПОЛЬЗОВАНИЕМ СДЕЛАЕЙТЕ РЕЗЕРВНУЮ КОПИЮ

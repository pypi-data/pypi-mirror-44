# Yatom

Beautiful HTML/XHTML/XML using YAML.

Yatom is a YAML to markup compiler supporting XML and HTML as output formats.

HTML and its siblings are not friendly at all, their very convoluted and often unreadable nature (due its parent: SGML) cannot be overtaken regardless on how much effort is put on both indentation and formatting. And even that requires further postprocessing to avoid the a huge size overhead.

In some way, Yatom shares the same concept as jedi/pugjs and HAML, but unless being *yaml-inspired*<sup>TM</sup>, Yatom is absolutely pure YAML, completely language agnostic, without extra stuff, requirements or incompatibilities.

YAML in, HTML out, simple.

## Usage

Simple HTML5 page using Yatom.

```python
import yatom

source = '''
  doctype: html5
  html:
    head:
      title: My Yatom page!
    body:
      h2: Yatom is awesome
      p: >-
        Now, you can code your page with
        beautiful markup without worrying
        about inefficient HTML output nor
        erratic linebreak behavior thanks
        to Yatom.
  '''
print(
  yatom.HTMLProcessor
    .from_source(source)
    .render()
  )
```

```html
<!DOCTYPE html>
<html><head><title>My Yatom page!</title></head><body><h2>Yatom is awesome</h2><p>Now, you can code your page with beautiful markup without worrying about inefficient HTML output nor erratic linebreak behavior thanks to Yatom.</p></body></html>
```


## The Yatom syntax

Yatom uses regular YAML, but that doesn't mean documents can of arbitrary shape.

The YAML document structure is defined by the target language, but mostly all follow the following rules:
- YAML root value must be a mapping.
- Nested mappings define the document structure.
- If a non-mapping value is is encountered, it is treated as a node value (text).

### HTML/XHTML/XML

The YAML syntax defining an entire HTML document is quite simple. If you already know HTML you can start writing Yatom templates with very few rules:
- Mapping keys are tag names.
  - doctypes are handled differently for convenience, and accepted values are listed here:
    - html4-strict
    - html4-transitional
    - html4-frameset
    - html5
    - xhtml1-strict
    - xhtml1-transitional
    - xhtml1-frameset
    - xhtml11
- Mapping string values are treated as text content.
- Dot-prefixed keys are tag attributes, must appear before any other tags, with some exceptions:
  - .text for inline text strings (escaped)
  - .literal for unescaped inlined text strings (allowing inline markup)
  - .cdata for XML CDATA tags
  - .comment for HTML comments

In addition to previous rules, tag attributes support nesting, with the following rules:
- When style value is a mapping, properties are treated as CSS properties, and nested mapping keys are joined with dashes (`-`).
- When class value is a mapping or list, its properties are treated as different classes (the dot is prefixed). It its a mapping its hierarchy (mapping or array) is combined with dashes (`-`).
- If any other attribute is a mapping or list, its hierarchy is combined with dashes (`-`).

And as a bonus, and only if required by doctype, few tags provide sane defaults:
- html4/xhtml
  - style type defaults to text/css
  - script type defaults to application/javascript
- xhtml
  - html has both default lang and xmlns
  - both style and script automatically wrap their content with CDATA

Semantic HTML rules are applied.

## Examples

Simple example for HTML5.

```python
import yatom

source = '''
  doctype: html5
  html:
    head:
      title: my page
    body:
      h2: my page
      p: |
        multiline
        text
      p:
        .text: mixed
        span:
          .style:
            color: red
          .text: tags
        .text: and
        strong: text
  '''
print(
  yatom.HTMLProcessor
    .from_source(source)
    .render()
  )
```

```html
<!DOCTYPE html>
<html><head><title>my page</title></head><body><h2>my page</h2><p>multiline
text
</p><p>mixed<span style="color:red">tags</span>and<strong>text</strong></p></body></html>
```

More advanced XHTML4 example.

```python
import yatom

source = '''
  doctype: xhtml11
  html:
    head:
      title: my page
      script: window.alert('<hello world>')
    body:
      .data:
        something: 1
        other: 2
      .class:
        - simple:
          - nested
        - other
      .style:
        padding:
          top: 2em
          bottom: 2em
          left: 25%
          right: 25%
      p: some simple text
  '''
print(
  yatom.HTMLProcessor
    .from_source(source)
    .render()
  )
```

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"><head><title>my page</title><script type="application/javascript"><![CDATA[window.alert('<hello world>')]]></script></head><body data-something="1" data-other="2" class="simple-nested other" style="padding-top:2em;padding-bottom:2em;padding-left:25%;padding-right:25%"><p>some simple text</p></body></html>
```

## Roadmap

- [ ] Pretty print
- [ ] Mustache-like logic
- [ ] Drop python2 for good

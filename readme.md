
# API Reference

### Generate Template

```http
  POST /api/template
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `templateName` | `string` | **Required**. Template Name |
| `title` | `Object` | **Required**. Paper Details |
| `authors` | `Array` | **Required**. Author Details |
| `content` | `Object` | **Required**. Content Details |

Here's Details values inside Each Parameter:

- templateName

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `templateName` | `string` | **Required**. Template Name - (APA7, IEEE, etc.) |

- title

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `paperName` | `string` | **Required**. Paper Name |
| `shorttitle` | `string` | **Optional**. Short Title (Recommended for APA7) |
| `course` | `string` | **Optional**. Course Name (Recommended for APA7) |
| `professor` | `string` | **Optional**. Professor Name (Recommended for APA7) |
| `footnotesize` | `string` | **Optional**. Foot Note |
| `thanks` | `string` | **Optional**. Thanking Note , used for Funding Agency |

- authors (Array of Objects)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. Author Name|
| `organization` | `string` | **Required**. Organization Name|
| `department` | `string` | **Optional**. Department Name|
| `city_country` | `string` | **Optional**. City & Country Name|
| `email` | `string` | **Optional**. Author email|

- content

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `sections` | `Array` | **Required**. Array of Sections containing (id,title,content and SubSections : [Optional - Array] {id,title,content and SubSubSections} : [Optional - Array] {id,title,contents }) |










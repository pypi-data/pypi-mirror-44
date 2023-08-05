# blogist

Generate personal blog posts from user's GitHub Gist.

## Install and usage

**Python3.7 needed**

`pip install blogist`

`blogist -n {GitHub_login_name}`

Your gists which file name has prefix '[blog]' with suffix '.md' will be downloaded in '_post/'. The prefix, suffix and directory can be customized.

## features

- [ ] build with CI/CD tools
- [ ] comments are extract from gist comments
- [ ] ~~use Jekyll, just like the default setting of GitHub Pages~~

## What can be extracted from Gist?

1. post name
2. created time
3. updated time
4. description
5. commonts
6. *categories [cate1,cate2,cate3...]*
7. *user GitHub profile*
8. *@ GitHub users*
9. *GitHub [octicons](https://octicons.github.com/)*

## Which one to choose?

| Generator     | Jekyll        | Hugo  | Hexo      |
|:-------------:|:-------------:|:-----:|:---------:|
| Language      | Ruby          | Go    |Javascript |
| Theme         | [Alembic](https://github.com/daviddarnes/alembic) | [Minimal](https://github.com/calintat/minimal) | [NexT](https://github.com/theme-next/hexo-theme-next) |
| Support       | :tada: | :x: | :x: |

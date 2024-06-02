from random import randint
from discord import Color, Embed, HTTPException, Message
from discord.ext.commands import Bot, Cog, Context, BucketType
import discord.ext.commands as Jeanne
from functions import (
    Hentai,
    check_botbanned_prefix,
    shorten_url,
    check_disabled_prefixed_command,
)
from assets.components import ReportContent, ReportContentPlus
from assets.argparsers import hentai_parser


class HentaiPrefix(Cog, name="Hentai"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        description="Get a random hentai from Jeanne",
        usage="<-r questionable | explicit | q | e> <-p Enable plus mode. Just type '-p'>",
    )
    @Jeanne.is_nsfw()
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.cooldown(1, 5, type=BucketType.user)
    async def hentai(self, ctx: Context, *words: str, parser=hentai_parser) -> None:
        try:
            parser = parser.parse_known_args(words)[0]
            rating = parser.rating
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        hentai, source = await Hentai().hentai(rating)
        is_mp4 = hentai.endswith("mp4")
        if is_mp4:
            view = ReportContent(shorten_url(hentai))
            m = await ctx.send(hentai, view=view)
        else:
            embed = (
                Embed(color=Color.purple())
                .set_image(url=hentai)
                .set_footer(
                    text="Fetched from {} • Credits must go to the artist".format(
                        source
                    )
                )
            )
            view = ReportContent(shorten_url(hentai))
            m: Message = await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value is None:
            await m.edit(view=None)

    @hentai.error
    async def hentai_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)
            return
        if isinstance(error, Jeanne.CommandOnCooldown):
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)

    @Jeanne.command(description="Get a random media content from Gelbooru")
    @Jeanne.is_nsfw()
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.cooldown(1, 5, type=BucketType.member)
    async def gelbooru(
        self,
        ctx: Context,
        *words: str,
        parser=hentai_parser,
    ) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            tags = "" if parsed_args.tags == None else " ".join(parsed_args.tags)
            rating: str = parsed_args.rating
            plus: bool = parsed_args.plus
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        image = await Hentai(plus).gelbooru(rating, tags)
        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            view = ReportContentPlus(*[img["file_url"] for img in images])
            vids = [i for i in images if "mp4" in i["file_url"]]
            media = [j["file_url"] for j in vids]
            imgs = [img["file_url"] for img in images]
            if media:
                m: Message = await ctx.send("\n".join(imgs), view=view)
                await view.wait()
                if view.value is None:
                    await m.edit(view=None)
                return
            color = Color.random()
            embeds = [
                Embed(color=color, url="https://gelbooru.com")
                .set_image(url=img["file_url"])
                .set_footer(
                    text="Fetched from Gelbooru • Credits must go to the artist"
                )
                for img in images
            ]
            m: Message = await ctx.send(embeds=embeds, view=view)
            await view.wait()
            if view.value is None:
                await m.edit(view=None)
            return
        try:
            view = ReportContent(image)
            if str(image).endswith("mp4"):
                m: Message = await ctx.send(image, view=view)
                await view.wait()
                if view.value is None:
                    await m.edit(view=None)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Fetched from Gelbooru • Credits must go to the artist"
                )
            )
            m: Message = await ctx.send(embed=embed, view=view)
            await view.wait()
            if view.value is None:
                await m.edit(view=None)
        except:
            if str(image).endswith("mp4"):
                await ctx.send(image)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Fetched from Gelbooru • Credits must go to the artist\nIf you see an illegal content, please use /botreport and attach the link when reporting"
                )
            )
            await ctx.send(embed=embed)

    @gelbooru.error
    async def gelbooru_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, ValueError, TypeError)
        ):
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)

    @Jeanne.command(description="Get a random hentai from Yande.re")
    @Jeanne.is_nsfw()
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.cooldown(1, 5, type=BucketType.member)
    async def yandere(self, ctx: Context, *words: str, parser=hentai_parser) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            tags = "" if parsed_args.tags == None else " ".join(parsed_args.tags)
            rating: str = parsed_args.rating
            plus: bool = parsed_args.plus
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        if tags == "02":
            await ctx.send(
                "Tag has been blacklisted due to it returning extreme content"
            )
            return
        image = await Hentai(plus).yandere(rating, tags)
        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            shortened_urls = [shorten_url(img["sample_url"]) for img in images]
            view = ReportContentPlus(*shortened_urls)
            color = Color.random()
            embeds = [
                Embed(color=color, url="https://files.yande.re")
                .set_image(url=url)
                .set_footer(
                    text="Fetched from Yande.re • Credits must go to the artist"
                )
                for url in shortened_urls
            ]
            footer_text = "Fetched from Yande.re • Credits must go to the artist"
            try:
                m: Message = await ctx.send(embeds=embeds, view=view)
                await view.wait()
                if view.value == None:
                    await m.edit(view=None)
            except:
                footer_text += "\nIf you see an illegal content, please use /botreport and attach the link when reporting"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.send(embeds=embeds)
            return
        color = Color.random()
        shortened_url = shorten_url(str(image))
        embed = Embed(color=color, url="https://files.yande.re")
        embed.set_image(url=shortened_url)
        footer_text = "Fetched from Yande.re • Credits must go to the artist"
        try:
            view = ReportContent(shortened_url)
            embed.set_footer(text=footer_text)
            m: Message = await ctx.send(embed=embed, view=view)
            await view.wait()
            if view.value == None:
                await m.edit(view=None)
        except:
            footer_text += "\nIf you see an illegal content, please use /botreport and attach the link when reporting"
            embed.set_footer(text=footer_text)
            await ctx.send(embed=embed)

    @yandere.error
    async def yandere_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, ValueError, TypeError)
        ):
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)

    @Jeanne.command(description="Get a random hentai from Konachan")
    @Jeanne.is_nsfw()
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.cooldown(1, 5, type=BucketType.member)
    async def konachan(self, ctx: Context, *words: str, parser=hentai_parser) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            tags = "" if parsed_args.tags == None else " ".join(parsed_args.tags)
            rating: str = parsed_args.rating
            plus: bool = parsed_args.plus
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        image = await Hentai(plus).konachan(rating, tags)
        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            try:
                shortened_urls = [shorten_url(img["file_url"]) for img in images]
                view = ReportContentPlus(*shortened_urls)
                color = Color.random()
                embeds = [
                    Embed(color=color, url="https://konachan.com")
                    .set_image(url=str(url))
                    .set_footer(
                        text="Fetched from Konachan • Credits must go to the artist"
                    )
                    for url in shortened_urls
                ]
                footer_text = "Fetched from Konachan • Credits must go to the artist"
                m: Message = await ctx.send(embeds=embeds, view=view)
                await view.wait()
                if view.value == None:
                    await m.edit(view=None)
            except:
                color = Color.random()
                embeds = [
                    Embed(color=color, url="https://konachan.com")
                    .set_image(url=str(url["image_url"]))
                    .set_footer(
                        text="Fetched from Konachan • Credits must go to the artist"
                    )
                    for url in images
                ]
                footer_text += "\nIf you see an illegal content, please use /botreport and attach the link when reporting"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.send(embeds=embeds)
            return
        color = Color.random()
        embed = Embed(color=color, url="https://konachan.com")
        embed.set_image(url=shorten_url(str(image)))
        footer_text = "Fetched from Konachan • Credits must go to the artist"
        try:
            view = ReportContent(shorten_url(str(image)))
            embed.set_footer(text=footer_text)
            m: Message = await ctx.send(embed=embed, view=view)
            await view.wait()
            if view.value == None:
                await m.edit(view=None)
        except:
            footer_text += "\nIf you see an illegal content, please use /botreport and attach the link when reporting"
            embed.set_footer(text=footer_text)
            await ctx.send(embed=embed)
            return

    @konachan.error
    async def konachan_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, ValueError, TypeError)
        ):
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)

    @Jeanne.command(description="Get a random media content from Danbooru")
    @Jeanne.is_nsfw()
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.cooldown(1, 5, type=BucketType.member)
    async def danbooru(self, ctx: Context, *words: str, parser=hentai_parser) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            tags = "" if parsed_args.tags == None else " ".join(parsed_args.tags)
            rating: str = parsed_args.rating
            plus: bool = parsed_args.plus
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        image = await Hentai(plus).danbooru(rating, tags)
        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            view = ReportContentPlus(*[img["file_url"] for img in images])
            vids = [i for i in images if "mp4" in i["file_url"]]
            media = [j["file_url"] for j in vids]
            imgs = [img["file_url"] for img in images]
            if media:
                m: Message = await ctx.send("\n".join(imgs), view=view)
                await view.wait()
                if view.value == None:
                    await m.edit(view=None)
                return
            color = Color.random()
            embeds = [
                Embed(color=color, url="https://danbooru.donmai.us/")
                .set_image(url=img["file_url"])
                .set_footer(
                    text="Fetched from Danbooru • Credits must go to the artist"
                )
                for img in images
            ]
            await ctx.send(embeds=embeds, view=view)
            return
        try:
            view = ReportContent(image)
            if str(image).endswith("mp4"):
                await ctx.send(image, view=view)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Fetched from Danbooru • Credits must go to the artist"
                )
            )
            m: Message = await ctx.send(embed=embed, view=view)
            await view.wait()
            if view.value == None:
                await m.edit(view=None)
        except:
            if str(image).endswith("mp4"):
                await ctx.send(image)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Fetched from Danbooru • Credits must go to the artist\nIf you see an illegal content, please use /botreport and attach the link when reporting"
                )
            )
            await ctx.send(embed=embed)

    @danbooru.error
    async def danbooru_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, ValueError, TypeError)
        ):
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)


async def setup(bot: Bot):
    await bot.add_cog(HentaiPrefix(bot))

package coffee.cypher.hexbound.feature.media_attachment

import at.petrak.hexcasting.api.misc.MediaConstants
import kotlinx.serialization.Serializable

@Serializable
data class StaticMediaValue(val priority: Int, val amount: Long, val unit: Unit) {
    enum class Unit(val calculate: (Long) -> Long) {
        ABSOLUTE({ it }),
        DUST(MediaConstants.DUST_UNIT::times),
        SHARD(MediaConstants.SHARD_UNIT::times),
        CRYSTAL(MediaConstants.CRYSTAL_UNIT::times)
    }

    val value get() = unit.calculate(amount)
}